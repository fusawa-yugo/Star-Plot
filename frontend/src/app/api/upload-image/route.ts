import { NextRequest, NextResponse } from "next/server";
import { writeFile, mkdir } from "fs/promises";
import { existsSync } from "fs";
import path from "path";

export async function POST(req: NextRequest) {
  const formData = await req.formData();
  const file = formData.get("file") as File;
  const filename = formData.get("filename") as string;

  if (!file || !filename) {
    return NextResponse.json({ error: "ファイルが見つかりません" }, { status: 400 });
  }

  const bytes = await file.arrayBuffer();
  const buffer = Buffer.from(bytes);

  const uploadDir = path.join(process.cwd(), "public/uploads");

  try {
    await mkdir(uploadDir, { recursive: true });

    const filePath = path.join(uploadDir, filename);

	if (existsSync(filePath)) {
		return NextResponse.json(
		  { error: "同じ名前のファイルがすでに存在します" },
		  { status: 409 } // 409 Conflict
		);
	}
    await writeFile(filePath, buffer);

	

	





    return NextResponse.json({
      message: "アップロード成功",
      filePath: `/uploads/${filename}`,
    });
  } catch (error) {
    console.error("ファイル保存エラー:", error);
    return NextResponse.json({ error: "保存に失敗しました" }, { status: 500 });
  }
}