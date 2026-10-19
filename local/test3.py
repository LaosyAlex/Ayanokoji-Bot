import subprocess

def _download_yt_dlp(url: str) -> list[str] | str:
    cmd = [
        "yt-dlp",
        "-v",
        "-P", r"local\temp",
        "--print", "after_move:filepath",
        "--cookies-from-browser", "firefox",
        str(url)
    ]

    result = subprocess.run([*cmd], capture_output=True, text=True, check=False)

    print("Exit code:", result.returncode)
    print("STDERR:", result.stderr)
    print("STDOUT:", result.stdout)

    '''
    if Extract._is_403(result.stderr):
        raise PermissionError("Request was blocked by site (DOWNLOAD).")
    '''

    if not result.stdout:
        raise ValueError("yt-dlp returned empty path")

    path = result.stdout



    return str(path).strip()

_download_yt_dlp("https://www.youtube.com/watch?v=Wto3Bzq7zeU")