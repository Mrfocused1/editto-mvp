import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Editto - AI Video Editor",
  description: "Edit videos with simple text instructions",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
