import json
from pathlib import Path

from specgen.agent_workflow import compile_prompt_pack
from specgen.contract_bundle import require


FIXTURE = Path(__file__).parent.parent / "prompt-packs" / "shared-contract-program" / "spec.json"


def test_native_pack_declares_exact_bundle_and_all_schema_digests():
    document = json.loads(FIXTURE.read_text(encoding="utf-8"))
    pack, _ = compile_prompt_pack(document)
    requirements = set(pack["workflow"]["requires"])

    version, digest = require("agent-workflow/prompt-pack/v2")
    assert f"contract-bundle=={version}" in requirements
    for schema_id in (
        "agent-workflow/prompt-pack/v2",
        "agent-workflow/evaluation-plan/v1",
        "agent-workflow/source-baseline/v1",
        "agent-workflow/agent-role/v1",
        "agent-workflow/task-result/v1",
    ):
        assert f"contract-schema-digest:{schema_id}={require(schema_id)[1]}" in requirements
    assert pack["schema"] == "agent-workflow/prompt-pack/v2"
    assert pack["bundle_provenance"] == {
        "bundle_version": version,
        "schema_id": "agent-workflow/prompt-pack/v2",
        "schema_digest": digest,
    }


def test_bundle_digest_declaration_is_not_substitutable():
    document = json.loads(FIXTURE.read_text(encoding="utf-8"))
    pack, _ = compile_prompt_pack(document)
    requires = pack["workflow"]["requires"]
    declaration = next(item for item in requires if item.startswith("contract-schema-digest:"))
    assert declaration.rsplit("=", 1)[1] != "invalid"
