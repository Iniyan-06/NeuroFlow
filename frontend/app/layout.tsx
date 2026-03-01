import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NeuroFlow OS",
  description: "Cognitive Load Redistribution — One clear action, always.",
  icons: { icon: "/favicon.ico" },
};

export const viewport: Viewport = {
  themeColor: "#0d0d10",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-dvh bg-[var(--background)] text-[var(--foreground)] antialiased">
        <div className="mx-auto w-full max-w-md md:max-w-3xl lg:max-w-5xl min-h-dvh flex flex-col">
          {children}
        </div>
      </body>
    </html>
  );
}
