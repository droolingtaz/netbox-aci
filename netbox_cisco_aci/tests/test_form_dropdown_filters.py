"""Regression guard: every `DynamicModel(Multiple)ChoiceField` whose
``queryset=`` is filtered server-side must also pass `query_params=`
so the API typeahead filters identically.

Background
----------

The first time a user saw the "Select a valid choice" message in the
v0.1.1 UI, it was on the **Add USeg Attribute** form: the field's
``queryset=ACIEndpointGroup.objects.filter(is_useg=True)`` restricts
the *server-side* validation to uSeg EPGs, but the dropdown's
typeahead hit the REST API (which has no ``is_useg`` default) and
happily showed every EPG. The user picked a non-uSeg EPG, hit Create,
and Django's form validation rejected the choice on submit. The fix
was to add ``query_params={"is_useg": True}`` so the API typeahead
filters identically to the queryset.

This test makes sure no future form regresses into the same shape:
for every ``DynamicModelChoiceField`` / ``DynamicModelMultipleChoiceField``
in the forms package whose queryset uses ``.filter(...)``, assert
``query_params`` is set. We don't require the *values* to match (that
would be too rigid) — only the presence, so a maintainer sees the
field looks intentional.

The check is static: it scans the forms source with a regex rather
than instantiating Django, so it runs in a fraction of a second and
needs no DB setup.
"""

from __future__ import annotations

import pathlib
import re

from django.test import SimpleTestCase

# Match the *start* of a ``identifier = DynamicModel(Multiple)?ChoiceField(``
# declaration. The body (everything up to the matching closing paren) is
# then extracted by a paren-counting walker rather than a regex, because
# a regex with balanced-paren alternation backtracks catastrophically on
# bodies that contain nested function calls like ``help_text=_("...")``.
_FIELD_START_PATTERN = re.compile(
    r"(?P<name>\w+)\s*=\s*DynamicModel(?:Choice|MultipleChoice)Field\("
)


def _extract_field_bodies(src: str):
    """Yield (match_start, name, body) tuples for every DynamicModel*ChoiceField
    declaration in ``src``. ``body`` is the substring between the opening
    ``(`` and the matching ``)`` of the field constructor — including any
    nested function calls.
    """
    for m in _FIELD_START_PATTERN.finditer(src):
        depth = 1
        i = m.end()
        n = len(src)
        # Skip past string literals so an unbalanced ``)`` inside a quoted
        # string can't fool the depth counter. We only need to handle the
        # quote styles the codebase actually uses.
        while i < n and depth > 0:
            c = src[i]
            if c == "(":
                depth += 1
                i += 1
            elif c == ")":
                depth -= 1
                i += 1
            elif c in ("'", '"'):
                quote = c
                # Triple-quoted string?
                if src[i : i + 3] == quote * 3:
                    end = src.find(quote * 3, i + 3)
                    i = (end + 3) if end != -1 else n
                else:
                    i += 1
                    while i < n and src[i] != quote:
                        if src[i] == "\\" and i + 1 < n:
                            i += 2
                        else:
                            i += 1
                    i += 1  # consume the closing quote
            else:
                i += 1
        # i is now one past the matching ')'. Body is between m.end() and i-1.
        if depth == 0:
            body = src[m.end() : i - 1]
            yield m.start(), m.group("name"), body


# Exclusion list: fields where we have inspected the situation and
# concluded that no API-side filter is needed (e.g. the API endpoint
# already filters by the same condition unconditionally, or the
# ``.filter()`` is purely about excluding the in-edit object from its
# own M2M choices). Add an entry with a one-line explanation.
_EXEMPT = {
    # (forms_module, field_name): "why"
}


class DynamicModelChoiceFiltersPropagateTests(SimpleTestCase):
    """Static scan of forms/*.py for the API-typeahead-mismatch bug."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.forms_dir = pathlib.Path(__file__).resolve().parent.parent / "forms"
        assert cls.forms_dir.is_dir(), f"forms dir not found: {cls.forms_dir}"

    def test_filtered_querysets_also_pass_query_params(self):
        offenders: list[tuple[str, str, str]] = []
        for path in sorted(self.forms_dir.glob("*.py")):
            src = path.read_text()
            for match_start, name, body in _extract_field_bodies(src):
                # Only fields whose queryset is restricted server-side
                # need API-side propagation. ``.all()`` is fine; a bare
                # ``.objects`` is fine.
                if ".filter(" not in body:
                    continue
                # Strip line comments before checking for the kwarg so we
                # don't false-pass on a comment that merely mentions the
                # word "query_params".
                stripped_body = re.sub(r"#[^\n]*", "", body)
                if re.search(r"\bquery_params\s*=\s*\{", stripped_body):
                    continue
                key = (path.name, name)
                if key in _EXEMPT:
                    continue
                line = src[:match_start].count("\n") + 1
                offenders.append((f"{path.name}:{line}", name, body[:200]))

        if offenders:
            msg = [
                "Found DynamicModelChoiceField(s) with a filtered queryset but no query_params.",
                "The dropdown's typeahead hits the REST API, which has no default for the",
                "filter, so users will see invalid choices and the form will reject their pick",
                "on submit. Add `query_params={...}` matching the queryset filter, or add the",
                "field to _EXEMPT in tests/test_form_dropdown_filters.py with a justification.",
                "",
                "Offenders:",
            ]
            for loc, name, body in offenders:
                msg.append(f"  {loc} :: {name}")
                msg.append(f"    body[:200]: {body!r}")
            self.fail("\n".join(msg))
