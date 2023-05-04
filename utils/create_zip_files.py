import zipfile
import shutil
import os
import constants

# ZIPファイルを保存するディレクトリ
lambda_function_dir = f'./{constants.LAMBDA_FUNCTION_DIR}'
zip_dir = f'./{constants.ZIP_DIR}'

if os.path.exists(zip_dir):
  shutil.rmtree(zip_dir)
os.makedirs(zip_dir)

# lambda_functionsディレクトリ内のすべての.pyファイルを検索
for file_name in os.listdir(lambda_function_dir):
    if file_name.endswith('.py'):
        # ZIPファイル名を作成
        zip_name = file_name[:-3] + '.zip'
        zip_path = os.path.join(zip_dir, zip_name)
        # ZIPファイルを作成
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(os.path.join(lambda_function_dir, file_name), file_name)

print(f"All files zipped successfully!:\n{[file_name for file_name in os.listdir(lambda_function_dir) if file_name.endswith('.py')]}")
