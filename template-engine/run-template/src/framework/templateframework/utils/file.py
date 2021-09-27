from pathlib import Path


def render_dir(
        render,
        origin_dir,
        target_dir,
        sub_dir_origin=None,
        sub_dir_target=None):
    origin_dir = Path(origin_dir)
    target_dir = Path(target_dir)
    if not target_dir.exists():
        target_dir.mkdir()

    current_dir = origin_dir
    if sub_dir_origin is not None:
        current_dir = origin_dir.joinpath(sub_dir_origin)

    for file in current_dir.iterdir():
        if sub_dir_origin is None:
            new_sub_dir_origin = Path(file.name)
        else:
            new_sub_dir_origin = sub_dir_origin.joinpath(file.name)
        if sub_dir_target is None:
            new_sub_dir_target = Path(render.render_folder_name(file))
        else:
            new_sub_dir_target = sub_dir_target.joinpath(
                render.render_folder_name(file))
        new_path = target_dir.joinpath(new_sub_dir_target)
        if file.is_dir():
            if not new_path.exists():
                new_path.mkdir(parents=True)
            render_dir(
                render,
                origin_dir,
                target_dir,
                new_sub_dir_origin,
                new_sub_dir_target)
        else:
            try:
                origin_dir.joinpath(new_sub_dir_origin).read_text()
            except Exception:
                bytes_data = origin_dir.joinpath(
                    new_sub_dir_origin).read_bytes()
                target_dir.joinpath(new_sub_dir_target).write_bytes(bytes_data)
                continue
            render.render_data(new_sub_dir_origin, new_sub_dir_target)
