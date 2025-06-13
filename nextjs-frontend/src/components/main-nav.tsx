'use client'

import * as React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

import { cn } from '@/lib/utils'
import { ThemeToggle } from './theme-toggle'

export function MainNav() {
  const pathname = usePathname()
  
  return (
    <div className="border-b">
      <div className="flex h-16 items-center px-4 container">
        <div className="mr-4 flex">
          <Link href="/" className="flex items-center space-x-2">
            <span className="font-bold text-xl">Ringan KB</span>
          </Link>
        </div>
        <nav className="flex items-center space-x-4 lg:space-x-6 mx-6">
          <Link
            href="/features"
            className={cn(
              "text-sm font-medium transition-colors hover:text-primary",
              pathname === "/features"
                ? "text-primary"
                : "text-muted-foreground"
            )}
          >
            Features
          </Link>
          <Link
            href="/kb-report"
            className={cn(
              "text-sm font-medium transition-colors hover:text-primary",
              pathname === "/kb-report"
                ? "text-primary"
                : "text-muted-foreground"
            )}
          >
            KB Report
          </Link>
          <Link
            href="/ai-flow"
            className={cn(
              "text-sm font-medium transition-colors hover:text-primary",
              pathname === "/ai-flow"
                ? "text-primary"
                : "text-muted-foreground"
            )}
          >
            AI Flow
          </Link>
        </nav>
        <div className="ml-auto flex items-center space-x-4">
          <ThemeToggle />
        </div>
      </div>
    </div>
  )
}