import { NextResponse } from "next/server";

const BACKEND_BASE_URL = process.env.BACKEND_BASE_URL || "http://127.0.0.1:8000";

export async function POST(req: Request) {
  try {
    const payload = await req.json();
    const backendResponse = await fetch(`${BACKEND_BASE_URL}/recommend`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      cache: "no-store",
    });

    const contentType = backendResponse.headers.get("content-type") || "";
    const isJson = contentType.includes("application/json");
    const body = isJson
      ? await backendResponse.json()
      : { detail: await backendResponse.text() };

    return NextResponse.json(body, { status: backendResponse.status });
  } catch (error) {
    return NextResponse.json(
      {
        detail: "Failed to reach recommendation backend.",
        error: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 502 }
    );
  }
}
