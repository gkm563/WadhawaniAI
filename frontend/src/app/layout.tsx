import type { Metadata } from "next"
import "@/styles/globals.css"

export const metadata: Metadata = {
  title: "PathPilot AI | Multilingual Employability Assistant",
  description: "A low-bandwidth, offline-ready career guidance and employability assistant for Tier-2/Tier-3 college students in India.",
  manifest: "/manifest.json",
  themeColor: "#2563eb",
  viewport: "width=device-width, initial-scale=1, maximum-scale=5",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        {/* Modern high-contrast typography subset from Google Fonts */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-screen flex flex-col">
        <main className="flex-1 w-full max-w-lg mx-auto bg-background px-4 py-6 shadow-sm border-x border-border md:max-w-xl">
          {children}
        </main>
      </body>
    </html>
  )
}
