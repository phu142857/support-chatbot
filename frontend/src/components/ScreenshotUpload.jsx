function ScreenshotUpload({ onFileSelect }) {
  const handleChange = (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    if (!file.type.startsWith("image/")) {
      return;
    }

    onFileSelect(file);
  };

  return (
    <label className="upload-button">
      📎

      <input
        type="file"
        accept="image/png,image/jpeg,image/webp"
        onChange={handleChange}
      />
    </label>
  );
}

export default ScreenshotUpload;