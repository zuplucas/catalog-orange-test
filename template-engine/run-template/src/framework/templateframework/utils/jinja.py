from jinja2 import Environment, select_autoescape

from templateframework.metadata import Metadata


def generate_env(metadata: Metadata):
    env = Environment(
        extensions=['jinja2_strcase.StrcaseExtension'],
        autoescape=select_autoescape(),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    for k, v in metadata.filters.items():
        env.filters[k] = v

    env_vars = metadata.inputs.copy()
    env_vars["target_path"] = metadata.target_path
    env_vars["inputs"] = metadata.inputs
    env_vars["sample"] = metadata.sample
    return env, env_vars


def render_text(text: str, metadata: Metadata):
    env, env_vars = generate_env(metadata)
    return env.from_string(text).render(env_vars)
