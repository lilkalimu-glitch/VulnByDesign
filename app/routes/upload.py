"""
Unrestricted File Upload lab.

VULNERABILITIES:
  - No file type validation
  - No file size limits
  - Uploaded files served directly (potential code execution)
  - Original filename preserved (path traversal potential)
"""

import os

from flask import Blueprint, render_template, request, flash, send_from_directory

bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "static", "uploads")


@bp.route("/")
def index():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    uploaded_files = os.listdir(UPLOAD_FOLDER)
    return render_template("labs/upload.html", files=uploaded_files)


@bp.route("/submit", methods=["POST"])
def submit():
    """Upload a file with no validation."""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    if "file" not in request.files:
        flash("No file provided.", "danger")
        return render_template("labs/upload.html", files=os.listdir(UPLOAD_FOLDER))

    file = request.files["file"]

    if file.filename == "":
        flash("No file selected.", "danger")
        return render_template("labs/upload.html", files=os.listdir(UPLOAD_FOLDER))

    # VULN: No file extension check
    # VULN: No content-type validation
    # VULN: No file size limit
    # VULN: Original filename used (path traversal possible)
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    flash(f"File '{file.filename}' uploaded successfully.", "success")
    uploaded_files = os.listdir(UPLOAD_FOLDER)
    return render_template("labs/upload.html", files=uploaded_files)


@bp.route("/files/<path:filename>")
def uploaded_file(filename):
    """Serve uploaded files directly."""
    # VULN: Serves any uploaded file without content-type restrictions
    return send_from_directory(UPLOAD_FOLDER, filename)
