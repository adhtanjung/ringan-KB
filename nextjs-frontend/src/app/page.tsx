import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { ThemeToggle } from '@/components/theme-toggle'
import { Badge } from '@/components/ui/badge'

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b shadow-sm bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-40">
        <div className="container flex h-16 items-center justify-between py-4 max-w-6xl mx-auto px-4">
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent dark:from-blue-400 dark:to-purple-400">Ringan Mental Health AI</h1>
          </div>
          <div className="flex items-center gap-4">
            <ThemeToggle />
          </div>
        </div>
      </header>
      
      <main className="container py-12 max-w-6xl mx-auto px-4">
        <section className="mb-16 text-center">
          <h1 className="text-5xl font-bold tracking-tight mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent dark:from-blue-400 dark:to-purple-400">Mental Health AI Assistant</h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            A comprehensive AI assistant for mental health support, utilizing a structured knowledge base with retrieval-augmented generation (RAG) capabilities.
          </p>
        </section>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <Card className="overflow-hidden border-2 transition-all hover:shadow-lg hover:-translate-y-1">
            <CardHeader className="pb-3">
              <CardTitle className="text-xl font-bold">Mental Health Features</CardTitle>
              <CardDescription className="text-sm mt-1.5">
                Interact with the AI assistant, take self-assessments, and get personalized suggestions.
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-2 px-6">
              <div className="flex flex-wrap gap-2 mb-4">
                <Badge variant="outline" className="bg-amber-100/50 dark:bg-amber-900/20 text-amber-800 dark:text-amber-300 border-amber-200 dark:border-amber-800">Problems.xlsx</Badge>
                <Badge variant="outline" className="bg-purple-100/50 dark:bg-purple-900/20 text-purple-800 dark:text-purple-300 border-purple-200 dark:border-purple-800">SelfAssessment.xlsx</Badge>
                <Badge variant="outline" className="bg-green-100/50 dark:bg-green-900/20 text-green-800 dark:text-green-300 border-green-200 dark:border-green-800">Suggestions.xlsx</Badge>
              </div>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Experience the AI assistant powered by a structured knowledge base derived from XLSX sheets.
                See how the knowledge base enhances the AI's ability to provide relevant support.
              </p>
            </CardContent>
            <CardFooter className="px-6 pt-2 pb-6">
              <Link href="/features" className="w-full">
                <Button className="w-full font-medium">Open Features</Button>
              </Link>
            </CardFooter>
          </Card>
          
          <Card className="overflow-hidden border-2 transition-all hover:shadow-lg hover:-translate-y-1">
            <CardHeader className="pb-3">
              <CardTitle className="text-xl font-bold">Knowledge Base Report</CardTitle>
              <CardDescription className="text-sm mt-1.5">
                View detailed reports on knowledge base usage and effectiveness.
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-2 px-6">
              <div className="flex flex-wrap gap-2 mb-4">
                <Badge variant="outline" className="bg-red-100/50 dark:bg-red-900/20 text-red-800 dark:text-red-300 border-red-200 dark:border-red-800">FeedbackPrompts.xlsx</Badge>
                <Badge variant="outline" className="bg-orange-100/50 dark:bg-orange-900/20 text-orange-800 dark:text-orange-300 border-orange-200 dark:border-orange-800">NextActions.xlsx</Badge>
              </div>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Monitor KB health, usage statistics, and feedback analysis. See how XLSX data updates
                improve AI response quality over time.
              </p>
            </CardContent>
            <CardFooter className="px-6 pt-2 pb-6">
              <Link href="/kb-report" className="w-full">
                <Button className="w-full font-medium" variant="outline">View Reports</Button>
              </Link>
            </CardFooter>
          </Card>
          
          <Card className="overflow-hidden border-2 transition-all hover:shadow-lg hover:-translate-y-1">
            <CardHeader className="pb-3">
              <CardTitle className="text-xl font-bold">AI Flow Visualization</CardTitle>
              <CardDescription className="text-sm mt-1.5">
                Explore the AI's end-to-end processing flow.
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-2 px-6">
              <div className="flex flex-wrap gap-2 mb-4">
                <Badge variant="outline" className="bg-blue-100/50 dark:bg-blue-900/20 text-blue-800 dark:text-blue-300 border-blue-200 dark:border-blue-800">FinetuningExamples.xlsx</Badge>
                <Badge variant="outline" className="bg-slate-100/50 dark:bg-slate-900/20 text-slate-800 dark:text-slate-300 border-slate-200 dark:border-slate-800">All XLSX Sources</Badge>
              </div>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Visualize how the AI processes user input, retrieves knowledge, and generates responses.
                See the impact of XLSX data on each stage of the AI flow.
              </p>
            </CardContent>
            <CardFooter className="px-6 pt-2 pb-6">
              <Link href="/ai-flow" className="w-full">
                <Button className="w-full font-medium" variant="outline">Explore Flow</Button>
              </Link>
            </CardFooter>
          </Card>
        </div>
      </main>
      
      <footer className="border-t py-6">
        <div className="container flex flex-col md:flex-row items-center justify-between">
          <p className="text-sm text-muted-foreground">
            &copy; {new Date().getFullYear()} Ringan Mental Health AI. All rights reserved.
          </p>
          <div className="flex items-center gap-4 mt-4 md:mt-0">
            <p className="text-sm text-muted-foreground">
              Last KB Update: <span className="font-medium">2023-12-15 14:30</span>
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}