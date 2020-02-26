from sys import argv

if len(argv) == 1:
    print('''\
zip file or directory:
  zipr "dir/name"                    : write to "dir/name.zip"
  zipr "dir/name" "dst_name"         : write to "dir/dst_name.zip"
  zipr "dir/name" "dst_dir"          : write to "dst_dir/name.zip"
  zipr "dir/name" "dst_dir/dst_name" : write to "dst_dir/dst_name.zip"
  {name} in `dst_name` replaced with `name`.
  {stem} in `dst_name` replaced with `name` without suffix.
  {time} in `dst_name` replaced with time-stamp (%Y-%m-%d_%H-%M-%S-%f).
  
  If done successfully, the last line to be printed will be the path of the created zip file.
  Otherwise, the last line to be printed will be empty.
''')

else:
    try:

        import os
        from datetime import datetime
        from pathlib import Path

        TIME_STAMP = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')

        src = Path(argv[1]).resolve(True)

        base_dir = src.parent

        os.chdir(base_dir)

        # <editor-fold desc="select destination (dst)">

        if len(argv) == 2:
            dst = src.with_suffix('.zip')
        else:
            raw: str = argv[2]

            raw = raw.format(
                stem=src.stem,
                name=src.name,
                time=TIME_STAMP,
            )

            dst = Path(raw).resolve()

            if dst.is_dir():
                dst = dst.joinpath(f'{src.stem}.zip')
            else:
                dst = dst.with_suffix('.zip')

        # </editor-fold>

        print(f'src: {src}')
        print(f'dst: {dst}')

        # <editor-fold desc="build bush command">

        cmd = ['zip']

        if src.is_dir():
            cmd.append('-r')

        cmd.append(f'"{dst}" "{src.relative_to(base_dir)}"')

        cmd = ' '.join(cmd)

        # </editor-fold>

        if os.system(cmd) == 0 and dst.is_file():
            print('zip ready:')
            print(f'{dst}')
        else:
            print('')

    except:
        from traceback import print_exc
        print_exc()
        print('')

########################################################################################################################
