export default function UploadPanel({ onUpload }) {
  const handleFileChange = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    await onUpload(file);
    event.target.value = "";
  };

  return (
    <div className="upload-panel">
      <label htmlFor="document-upload">Upload banking docs</label>
      <input id="document-upload" type="file" accept=".txt,.pdf,.docx" onChange={handleFileChange} />
    </div>
  );
}
