---
orphan: true
---

# pccx vX.Y.Z - release notes

> **Release status.** Replace this paragraph with the release state:
> draft, prerelease, latest release, or archived release. Keep this page
> aligned with the GitHub Release body after publication.

- **Repo**: `pccxai/pccx`
- **Tag**: `vX.Y.Z`
- **Title**: `pccx vX.Y.Z - <short release subtitle>`
- **Pre-release**: yes/no
- **Release link**: <https://github.com/pccxai/pccx/releases/tag/vX.Y.Z>
- **Published**: YYYY-MM-DD

## Highlights

- <User-visible documentation, architecture, ISA, tooling, or release
  process change.>
- <Second highlight.>
- <Third highlight.>

## Compatibility

- **Documentation site**: <Sphinx/Furo/MyST compatibility notes, if any.>
- **RTL reference**: <Referenced RTL repo, branch/tag, and commit SHA.>
- **ISA PDF**: <PDF artifact status and source commit, if applicable.>
- **Migration impact**: <None, or describe required user action.>

## Validation status

- `make strict`: <pass/fail/not run; include date or CI run if useful.>
- `make lint`: <pass/fail/not run.>
- `make linkcheck`: <pass/fail/not run; weekly cron is acceptable for
  low-risk documentation-only releases.>
- GitHub Pages deploy: <pass/fail/not applicable.>
- GitHub Release artifacts: <published/not published/not applicable.>

## Known limitations

- <Current limitation, caveat, or measurement gap.>
- <Second limitation.>
- <Third limitation.>

## Not included in this release

- <Explicitly deferred work item.>
- <Second deferred item.>

## Next milestones

- `vX.Y+1.0`: <Planned theme or scope.>
- `vX.Y+2.0`: <Planned theme or scope.>

## Release checklist

- [ ] Update `CHANGELOG.md`.
- [ ] Add or refresh `docs/releases/vX.Y.Z.md` from this template.
- [ ] Confirm `CITATION.cff` is still accurate.
- [ ] If `main.tex` changed, run `bash tools/build_isa_pdf.sh` and
      commit `_static/downloads/pccx-isa-v002.pdf`.
- [ ] Run `make strict`.
- [ ] Publish the GitHub Release and copy the final release body back
      into `docs/releases/vX.Y.Z.md`.
