import os
import subprocess
import sys
import tempfile
import zipfile


def create_zip_files(lambda_function_dir, zip_dir, venv_dir):
    if not os.path.exists(zip_dir):
        os.makedirs(zip_dir)

    site_packages = os.path.join(
        venv_dir,
        "lib",
        f"python{sys.version_info.major}.{sys.version_info.minor}",
        "site-packages",
    )

    # lambda_functionsディレクトリ内のすべての.pyファイルを検索
    for file_name in os.listdir(lambda_function_dir):
        if file_name.endswith(".py"):
            # ZIPファイル名を作成
            zip_name = file_name[:-3] + ".zip"
            zip_path = os.path.join(zip_dir, zip_name)

            # 一時ディレクトリを作成して、依存関係をインストール
            with tempfile.TemporaryDirectory() as temp_dir:
                subprocess.check_call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "-r",
                        "requirements.txt",
                        "-t",
                        temp_dir,
                    ]
                )

                # ZIPファイルを作成
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                    # ラムダ関数を追加
                    zipf.write(os.path.join(lambda_function_dir, file_name), file_name)

                    # 依存関係を追加
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            zipf.write(
                                os.path.join(root, file),
                                os.path.relpath(os.path.join(root, file), temp_dir),
                            )
                    for root, dirs, files in os.walk(site_packages):
                        for file in files:
                            zipf.write(
                                os.path.join(root, file),
                                os.path.relpath(
                                    os.path.join(root, file), site_packages
                                ),
                            )


if __name__ == "__main__":
    import constants

    # ZIPファイルを保存するディレクトリ
    lambda_function_dir = f"./{constants.LAMBDA_FUNCTION_DIR}"
    zip_dir = f"./{constants.ZIP_DIR}"

    create_zip_files(lambda_function_dir, zip_dir, "venv")
