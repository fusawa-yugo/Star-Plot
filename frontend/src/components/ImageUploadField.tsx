"use client";
import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

const ImageUploadField = () => {
  const [uploadedImage, setUploadedImage] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setUploadedImage(acceptedFiles[0]);
    }
  }, []);

  const handleUpload = async () => {
    if (!uploadedImage) {
			alert("画像を選択してください");
			return;
		}

    const formData = new FormData();
    formData.append("file", uploadedImage);
		formData.append("filename", uploadedImage.name);

    try {
      setUploadStatus("アップロード中...");
      const response = await fetch("/api/upload-image", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        setUploadStatus("アップロード成功！");
      } else {
        setUploadStatus("アップロード失敗...");
      }
    } catch (error) {
      console.error("アップロードエラー", error);
      setUploadStatus("アップロード失敗");
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
  });

  return (
    <div className="flex flex-col items-center mx-2">
      <div className="flex flex-col items-center my-3">
        <div
          {...getRootProps()}
          className={`border-2 border-dashed p-3 rounded-md  ${
            isDragActive ? "border-blue-500" : "border-gray-300"
          }`}
        >
            <input {...getInputProps()} />
            <p className="text-xs">
              {isDragActive
                ? "ここにドロップしてください"
                : "画像をドラッグ＆ドロップするか、クリックして選択してください"}
            </p>
        </div>
        {uploadedImage && (
          <div className="mt-4 w-full">
            <p className="text-sm">アップロードされた画像:</p>
            <div className="flex flex-col items-center w-full h-[300px] border-2 rounded-lg bg-gray-100 box-border p-1">
              <img
                src={URL.createObjectURL(uploadedImage)}
                alt="Uploaded"
                className="max-w-full max-h-full"
              />
            </div>
          </div>
        )}
      </div>
      {uploadedImage && (
        <button
          onClick={handleUpload}
          className="text-sm mt-1 px-4 py-2 bg-blue-300 rounded-md text-black self-end"
        >
          画像を送信
        </button>
      )}
      {uploadStatus && <p className="mt-2">{uploadStatus}</p>}
    </div>
  );
};

export default ImageUploadField;
