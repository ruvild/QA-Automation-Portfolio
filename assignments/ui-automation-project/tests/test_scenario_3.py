from utils.file_helpers import wait_for_download, extract_size_mb
from selene import have, query


def test_download(saby_main, download_manager):
    app_name = "Saby Center"

    saby_downloads = saby_main.go_to_downloads()

    download_dir, old_files = download_manager
    saby_downloads.download_file(app_name)
    downloaded_file_path = wait_for_download(download_dir, old_files)

    assert downloaded_file_path.exists()

    actual_file_size = round(downloaded_file_path.stat().st_size / (1024 * 1024), 2)
    ui_file_size = extract_size_mb(
        saby_downloads.download_link(app_name).get(query.text)
    )

    assert round(actual_file_size, 2) == round(ui_file_size, 2)
