import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Indecisive",
  description: "Not sure what to eat? Tell us your mood. We'll find nearby places."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
