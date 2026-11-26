# The project contract's two targets, in the factory plugin's project-contract.md.
.PHONY: setup check

# --locked fails when uv.lock doesn't match pyproject.toml, so setup never rewrites uv.lock, which
# the contract doesn't allow.
setup:
	uv sync --locked

check:
	bash tools/check-code.sh
