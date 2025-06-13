'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
// Remove unused Badge import since the component is not being used
import { getKBStats, getKBUsageReport } from '@/lib/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

export default function KBReportPage() {
  const { data: kbStats, isLoading: isLoadingStats } = useQuery({
    queryKey: ['kb-stats'],
    queryFn: getKBStats,
  })

  const { data: usageReport, isLoading: isLoadingReport } = useQuery({
    queryKey: ['kb-usage-report'],
    queryFn: getKBUsageReport,
  })

  if (isLoadingStats || isLoadingReport) {
    return (
      <div className="container py-6">
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center space-y-4">
            <div className="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full mx-auto"></div>
            <p className="text-muted-foreground">Loading knowledge base statistics...</p>
          </div>
        </div>
      </div>
    )
  }

  if (!kbStats || !usageReport) {
    return (
      <div className="container py-6">
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center space-y-4">
            <p className="text-lg text-muted-foreground">Failed to load knowledge base statistics.</p>
            <p className="text-sm text-muted-foreground">Please try refreshing the page.</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container py-6">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Problems</CardTitle>
            <CardDescription>Total problems in knowledge base</CardDescription>
          </CardHeader>
          <CardContent className="text-4xl font-bold">{kbStats.problems_count}</CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Suggestions</CardTitle>
            <CardDescription>Total suggestions available</CardDescription>
          </CardHeader>
          <CardContent className="text-4xl font-bold">{kbStats.suggestions_count}</CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Assessments</CardTitle>
            <CardDescription>Self-assessment questions</CardDescription>
          </CardHeader>
          <CardContent className="text-4xl font-bold">{kbStats.assessments_count}</CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Feedback Prompts</CardTitle>
            <CardDescription>Available feedback prompts</CardDescription>
          </CardHeader>
          <CardContent className="text-4xl font-bold">{kbStats.feedback_prompts_count}</CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Next Actions</CardTitle>
            <CardDescription>Defined next actions</CardDescription>
          </CardHeader>
          <CardContent className="text-4xl font-bold">{kbStats.next_actions_count}</CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Fine-tuning Examples</CardTitle>
            <CardDescription>Training examples</CardDescription>
          </CardHeader>
          <CardContent className="text-4xl font-bold">{kbStats.finetuning_examples_count}</CardContent>
        </Card>
      </div>

      <Tabs defaultValue="usage">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="usage">Usage Statistics</TabsTrigger>
          <TabsTrigger value="feedback">Feedback Analysis</TabsTrigger>
          <TabsTrigger value="sync">XLSX Sync History</TabsTrigger>
        </TabsList>

        <TabsContent value="usage" className="space-y-6">
          {/* Problem Usage Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Problem Usage Frequency</CardTitle>
              <CardDescription>
                <span className="xlsx-badge xlsx-badge-problems">Problems.xlsx</span>
                <span className="text-xs text-muted-foreground ml-2">Last updated: {new Date(kbStats.last_updated).toLocaleDateString()}</span>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={usageReport.problem_usage}
                    margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="count" name="Access Count" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          {/* Suggestion Effectiveness Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Suggestion Effectiveness</CardTitle>
              <CardDescription>
                <span className="xlsx-badge xlsx-badge-suggestions">Suggestions.xlsx</span>
                <span className="text-xs text-muted-foreground ml-2">Last updated: {new Date(kbStats.last_updated).toLocaleDateString()}</span>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={usageReport.suggestion_effectiveness}
                    margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis domain={[0, 5]} />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="rating" name="Average Rating" fill="#82ca9d" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="feedback" className="space-y-6">
          {/* Feedback Sentiment Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Feedback Sentiment Analysis</CardTitle>
              <CardDescription>
                <span className="xlsx-badge xlsx-badge-feedback">FeedbackPrompts.xlsx</span>
                <span className="text-xs text-muted-foreground ml-2">Last updated: {new Date(kbStats.last_updated).toLocaleDateString()}</span>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80 flex items-center justify-center">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={usageReport.feedback_sentiment}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {usageReport.feedback_sentiment.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          {/* Correlation Report */}
          <Card>
            <CardHeader>
              <CardTitle>KB Update Impact Analysis</CardTitle>
              <CardDescription>
                Correlation between XLSX updates and AI response quality
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 border rounded-md">
                  <div>
                    <h4 className="font-medium">Depression Suggestions Update</h4>
                    <p className="text-sm text-muted-foreground">Oct 28, 2023</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-green-600">+24% Satisfaction</p>
                    <p className="text-sm text-muted-foreground">Based on 78 feedback entries</p>
                  </div>
                </div>

                <div className="flex items-center justify-between p-4 border rounded-md">
                  <div>
                    <h4 className="font-medium">Anxiety Assessment Questions</h4>
                    <p className="text-sm text-muted-foreground">Nov 30, 2023</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-green-600">+18% Accuracy</p>
                    <p className="text-sm text-muted-foreground">Based on 45 assessments</p>
                  </div>
                </div>

                <div className="flex items-center justify-between p-4 border rounded-md">
                  <div>
                    <h4 className="font-medium">Finetuning Examples Addition</h4>
                    <p className="text-sm text-muted-foreground">Nov 15, 2023</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-green-600">+15% Empathy Rating</p>
                    <p className="text-sm text-muted-foreground">Based on 120 conversations</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="sync">
          {/* XLSX Sync History */}
          <Card>
            <CardHeader>
              <CardTitle>XLSX Sync History</CardTitle>
              <CardDescription>
                Record of knowledge base updates from XLSX files
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {usageReport.sync_history.map((entry, index) => (
                  <div key={index} className="flex items-start border-b last:border-0 pb-4 last:pb-0">
                    <div className="mr-4 p-2 bg-muted rounded-full">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M12 2v10l4.24 4.24" />
                        <circle cx="12" cy="12" r="10" />
                      </svg>
                    </div>
                    <div>
                      <p className="font-medium">{entry.date}</p>
                      <p className="text-sm text-muted-foreground">{entry.changes}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
            <CardFooter>
              <p className="text-sm text-muted-foreground">
                Last full sync: {new Date(kbStats.last_updated).toLocaleString()}
              </p>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}