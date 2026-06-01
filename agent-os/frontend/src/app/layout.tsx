import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'AgentOS - AI Agent Operating System',
  description: 'Create and manage your AI agent team for task automation',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
