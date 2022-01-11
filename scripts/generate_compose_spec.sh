pip install datamodel-code-generator[http]

# --url: Official Docker Compose spec at https://github.com/compose-spec/compose-spec
# --input: File from compose-spec is a JSON schema
# --output: Put it in with the other models
# --snake-case-field: All fields are already snake case, but this ensure that they are
# --field-constraints: Use field constraints instead of weird con* annotations
# --disable-timestamp: Don't add timestamp at top of generated file
# --strip-default-none: If something is labeled Optional remove the `=None`
# --enum-fields-as-literal one: If there is an enum with a single field just turn that into a literal, otherwise use enums
rm -f ../emulation_system/emulation_system/compose_file_creator/output/compose_file_model.py
touch ../emulation_system/emulation_system/compose_file_creator/output/compose_file_model.py

datamodel-codegen \
  --url https://raw.githubusercontent.com/compose-spec/compose-spec/master/schema/compose-spec.json \
  --input-file-type jsonschema \
  --output ../emulation_system/emulation_system/compose_file_creator/output/compose_file_model.py \
  --snake-case-field \
  --field-constraints \
  --strip-default-none \
  --enum-field-as-literal one

sed -i '/constr(/ s/$/  # type: ignore [valid-type]/' ../emulation_system/emulation_system/compose_file_creator/output/compose_file_model.py
