
import boto3
from botocore.exceptions import ClientError
from pathlib import Path

REGION = "ap-south-1"
BUCKET_NAME = "aws-sdk-static-site-cloudsite4829"
WEBSITE_DIR = Path("website")

def deploy_website():
    session = boto3.Session(profile_name="static-website")
    s3 = session.client("s3", region_name=REGION)

    if not WEBSITE_DIR.exists():
        print("Error: website folder not found.")
        return

    files = list(WEBSITE_DIR.rglob("*"))

    try:
        for file_path in files:
            if file_path.is_file():
                key = file_path.relative_to(WEBSITE_DIR).as_posix()

                content_type = (
                    "text/html" if file_path.suffix.lower() == ".html"
                    else "text/css" if file_path.suffix.lower() == ".css"
                    else "application/javascript"
                    if file_path.suffix.lower() == ".js"
                    else "application/octet-stream"
                )

                s3.upload_file(
                    str(file_path),
                    BUCKET_NAME,
                    key,
                    ExtraArgs={"ContentType": content_type}
                )

                print("Uploaded:", key)

        print("\nDeployment completed successfully!")
        print(
            "Website:",
            f"http://{BUCKET_NAME}.s3-website.{REGION}.amazonaws.com"
        )

    except (ClientError, OSError) as error:
        print("Deployment failed:", error)

if __name__ == "__main__":
    deploy_website()