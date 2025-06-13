'use client'

import { useState, useEffect, useRef } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Separator } from '@/components/ui/separator'
import { Badge } from '@/components/ui/badge'
import { Slider } from '@/components/ui/slider'
import { Label } from '@/components/ui/label'
import { getProblems, getSuggestions, getSelfAssessments, sendChatMessage, submitFeedback } from '@/lib/api'
import type { ChatMessage, Problem, Suggestion, SelfAssessment } from '@/lib/api'
import { format } from 'date-fns'

export default function FeaturesPage() {
  // State
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'ai',
      content: 'Hello! I\'m your mental health assistant. How can I help you today?',
      timestamp: new Date().toISOString(),
    },
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [selectedProblem, setSelectedProblem] = useState<Problem | null>(null)
  const [feedbackText, setFeedbackText] = useState('')
  const [currentAssessment, setCurrentAssessment] = useState<SelfAssessment | null>(null)
  const [assessmentResponse, setAssessmentResponse] = useState<Record<string, any>>({}) 
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Queries
  const { data: problems = [] } = useQuery({
    queryKey: ['problems'],
    queryFn: getProblems,
  })

  const { data: suggestions = [] } = useQuery({
    queryKey: ['suggestions', selectedProblem?.id],
    queryFn: () => getSuggestions(selectedProblem?.id),
    enabled: !!selectedProblem,
  })

  const { data: assessments = [] } = useQuery({
    queryKey: ['assessments', selectedProblem?.id],
    queryFn: () => getSelfAssessments(selectedProblem?.id),
    enabled: !!selectedProblem,
  })

  // Effects
  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Functions
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return

    setIsLoading(true)
    // Add user message to chat
    const userMessage: ChatMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
    }
    setMessages(prev => [...prev, userMessage])
    setInputMessage('')

    try {
      // Send message to API
      const response = await sendChatMessage({
        message: inputMessage,
        session_id: sessionId || undefined,
        context: selectedProblem ? { problem_id: selectedProblem.id } : undefined,
      })

      // Update session ID if not set
      if (!sessionId) {
        setSessionId(response.session_id)
      }

      // Add AI response to chat
      const aiMessage: ChatMessage = {
        role: 'ai',
        content: response.response,
        timestamp: new Date().toISOString(),
        metadata: {
          problem_id: response.metadata?.problem_id,
          kb_source: response.metadata?.kb_source,
          source_documents: response.metadata?.source_documents,
          last_updated: '2023-12-15', // This would come from the API in a real implementation
        },
      }
      setMessages(prev => [...prev, aiMessage])

      // If problem ID is returned, select that problem
      if (response.metadata?.problem_id) {
        const problem = problems.find(p => p.id === response.metadata?.problem_id)
        if (problem) setSelectedProblem(problem)
      }
    } catch (error) {
      console.error('Error sending message:', error)
      // Add error message
      setMessages(prev => [
        ...prev,
        {
          role: 'ai',
          content: 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date().toISOString(),
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmitFeedback = async () => {
    if (!feedbackText.trim() || !sessionId) return

    try {
      // Get last user and AI messages
      const lastUserMessage = [...messages].reverse().find(m => m.role === 'user')?.content
      const lastAiMessage = [...messages].reverse().find(m => m.role === 'ai')?.content

      await submitFeedback({
        feedback: feedbackText,
        session_id: sessionId,
        user_message: lastUserMessage,
        ai_response: lastAiMessage,
        problem_id: selectedProblem?.id,
      })

      // Clear feedback and add confirmation message
      setFeedbackText('')
      setMessages(prev => [
        ...prev,
        {
          role: 'ai',
          content: 'Thank you for your feedback! It helps me improve.',
          timestamp: new Date().toISOString(),
        },
      ])
    } catch (error) {
      console.error('Error submitting feedback:', error)
    }
  }

  const startAssessment = (assessment: SelfAssessment) => {
    setCurrentAssessment(assessment)
    setAssessmentResponse({})
  }

  const handleAssessmentResponse = (value: any) => {
    setAssessmentResponse({ ...assessmentResponse, [currentAssessment?.question_id || '']: value })
  }

  const submitAssessmentResponse = () => {
    // In a real implementation, this would send the response to the API
    // For now, we'll just add it to the chat
    if (!currentAssessment) return

    const responseValue = assessmentResponse[currentAssessment.question_id]
    let responseText = ''

    if (currentAssessment.response_type === 'scale_1_5') {
      responseText = `${responseValue}/5`
    } else if (currentAssessment.response_type === 'yes_no') {
      responseText = responseValue ? 'Yes' : 'No'
    } else {
      responseText = responseValue
    }

    // Add assessment question and response to chat
    setMessages(prev => [
      ...prev,
      {
        role: 'ai',
        content: currentAssessment.question_text,
        timestamp: new Date().toISOString(),
        metadata: {
          kb_source: 'SelfAssessment.xlsx',
          last_updated: '2023-12-15',
        },
      },
      {
        role: 'user',
        content: `My response: ${responseText}`,
        timestamp: new Date().toISOString(),
      },
    ])

    // Clear current assessment
    setCurrentAssessment(null)
  }

  const renderSourceDocuments = (metadata?: ChatMessage['metadata']) => {
    if (!metadata?.source_documents?.length) return null

    return (
      <div className="mt-2 text-sm text-muted-foreground">
        <p className="font-medium">Sources:</p>
        <ul className="list-disc list-inside space-y-1">
          {metadata.source_documents.map((doc, index) => (
            <li key={index}>{doc}</li>
          ))}
        </ul>
      </div>
    )
  }

  return (
    <div className="container py-6">
      <h1 className="text-3xl font-bold mb-6">Mental Health AI Assistant</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          {/* Problems Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                Problems
                <Badge variant="outline" className="ml-2 text-xs">
                  <span className="xlsx-badge xlsx-badge-problems">Problems.xlsx</span>
                </Badge>
              </CardTitle>
              <CardDescription>Select a problem to explore</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {problems.map((problem) => (
                  <Button 
                    key={problem.id}
                    variant={selectedProblem?.id === problem.id ? "default" : "outline"}
                    className="w-full justify-start text-left"
                    onClick={() => setSelectedProblem(problem)}
                  >
                    {problem.problem_name}
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Self-Assessment Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                Self-Assessments
                <Badge variant="outline" className="ml-2 text-xs">
                  <span className="xlsx-badge xlsx-badge-assessment">SelfAssessment.xlsx</span>
                </Badge>
              </CardTitle>
              <CardDescription>
                Take an assessment related to {selectedProblem?.problem_name || 'a problem'}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {selectedProblem ? (
                assessments.length > 0 ? (
                  <div className="space-y-2">
                    {assessments.map((assessment) => (
                      <Button
                        key={assessment.question_id}
                        variant="outline"
                        className="w-full justify-start text-left"
                        onClick={() => startAssessment(assessment)}
                      >
                        {assessment.question_text.substring(0, 30)}...
                      </Button>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-muted-foreground">No assessments available for this problem.</p>
                )
              ) : (
                <p className="text-sm text-muted-foreground">Select a problem to see available assessments.</p>
              )}
            </CardContent>
          </Card>

          {/* Suggestions Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                Suggestions
                <Badge variant="outline" className="ml-2 text-xs">
                  <span className="xlsx-badge xlsx-badge-suggestions">Suggestions.xlsx</span>
                </Badge>
              </CardTitle>
              <CardDescription>
                Helpful resources for {selectedProblem?.problem_name || 'mental health'}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {selectedProblem ? (
                suggestions.length > 0 ? (
                  <div className="space-y-3">
                    {suggestions.map((suggestion) => (
                      <div key={suggestion.suggestion_id} className="p-3 border rounded-md">
                        <p className="text-sm">{suggestion.suggestion_text}</p>
                        {suggestion.resource_link && (
                          <a 
                            href={suggestion.resource_link} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-xs text-blue-500 hover:underline mt-1 block"
                          >
                            Learn more
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-muted-foreground">No suggestions available for this problem.</p>
                )
              ) : (
                <p className="text-sm text-muted-foreground">Select a problem to see suggestions.</p>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3">
          <Tabs defaultValue="chat">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="chat">Chat with AI</TabsTrigger>
              <TabsTrigger value="kb-info">Knowledge Base Info</TabsTrigger>
            </TabsList>
            
            <TabsContent value="chat" className="space-y-4">
              {/* Chat Card */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <div>Chat with AI Assistant</div>
                    {sessionId && (
                      <Badge variant="outline">Session: {sessionId.substring(0, 8)}...</Badge>
                    )}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {/* Assessment Modal */}
                  {currentAssessment && (
                    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                      <Card className="w-full max-w-md">
                        <CardHeader>
                          <CardTitle>Self-Assessment</CardTitle>
                          <CardDescription>
                            <span className="xlsx-badge xlsx-badge-assessment">SelfAssessment.xlsx</span>
                            <span className="text-xs text-muted-foreground ml-2">Last updated: 2023-12-15</span>
                          </CardDescription>
                        </CardHeader>
                        <CardContent>
                          <p className="mb-4">{currentAssessment.question_text}</p>
                          
                          {currentAssessment.response_type === 'scale_1_5' && (
                            <div className="space-y-4">
                              <Slider
                                defaultValue={[3]}
                                min={1}
                                max={5}
                                step={1}
                                onValueChange={(value) => handleAssessmentResponse(value[0])}
                              />
                              <div className="flex justify-between text-xs text-muted-foreground">
                                <span>1 - Not at all</span>
                                <span>3 - Somewhat</span>
                                <span>5 - Extremely</span>
                              </div>
                            </div>
                          )}
                          
                          {currentAssessment.response_type === 'yes_no' && (
                            <div className="flex gap-4">
                              <Button 
                                variant="outline" 
                                onClick={() => handleAssessmentResponse(true)}
                                className={assessmentResponse[currentAssessment.question_id] === true ? 'bg-primary text-primary-foreground' : ''}
                              >
                                Yes
                              </Button>
                              <Button 
                                variant="outline"
                                onClick={() => handleAssessmentResponse(false)}
                                className={assessmentResponse[currentAssessment.question_id] === false ? 'bg-primary text-primary-foreground' : ''}
                              >
                                No
                              </Button>
                            </div>
                          )}
                          
                          {currentAssessment.response_type === 'text' && (
                            <Textarea
                              placeholder="Type your response here..."
                              onChange={(e) => handleAssessmentResponse(e.target.value)}
                            />
                          )}
                        </CardContent>
                        <CardFooter className="flex justify-between">
                          <Button variant="outline" onClick={() => setCurrentAssessment(null)}>Cancel</Button>
                          <Button onClick={submitAssessmentResponse}>Submit</Button>
                        </CardFooter>
                      </Card>
                    </div>
                  )}
                  
                  {/* Chat Messages */}
                  <div className="chat-container">
                    {messages.map((message, index) => (
                      <div 
                        key={index} 
                        className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} mb-4`}
                      >
                        <div className={`rounded-lg px-4 py-2 max-w-[80%] ${message.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}>
                          <p>{message.content}</p>
                          {message.metadata?.kb_source && (
                            <p className="mt-1 text-xs opacity-70">
                              Source: {message.metadata.kb_source}
                              {message.metadata.last_updated && (
                                <span> (Last updated: {message.metadata.last_updated})</span>
                              )}
                            </p>
                          )}
                          {message.metadata?.source_documents && (
                            <div className="mt-2 space-y-1">
                              <p className="text-xs font-medium">Source Documents:</p>
                              {message.metadata.source_documents.map((doc, idx) => (
                                <div key={idx} className="text-xs bg-secondary/50 p-2 rounded">
                                  <p>{doc.content}</p>
                                  {doc.metadata && (
                                    <p className="mt-1 opacity-70">
                                      {Object.entries(doc.metadata).map(([key, value]) => (
                                        <span key={key} className="mr-2">
                                          {key}: {value}
                                        </span>
                                      ))}
                                    </p>
                                  )}
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                    <div ref={messagesEndRef} />
                  </div>
                </CardContent>
                <CardFooter>
                  <div className="flex w-full items-center space-x-2">
                    <Input
                      type="text"
                      placeholder="Type your message..."
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    />
                    <Button onClick={handleSendMessage} disabled={isLoading}>
                      {isLoading ? (
                        <svg
                          className="animate-spin h-4 w-4"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle
                            className="opacity-25"
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="currentColor"
                            strokeWidth="4"
                          />
                          <path
                            className="opacity-75"
                            fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                          />
                        </svg>
                      ) : 'Send'}
                    </Button>
                  </div>
                </CardFooter>
              </Card>

              {/* Feedback Card */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    Provide Feedback
                    <Badge variant="outline" className="ml-2 text-xs">
                      <span className="xlsx-badge xlsx-badge-feedback">FeedbackPrompts.xlsx</span>
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Textarea
                    placeholder="Share your thoughts about the AI's response..."
                    value={feedbackText}
                    onChange={(e) => setFeedbackText(e.target.value)}
                  />
                </CardContent>
                <CardFooter>
                  <Button 
                    onClick={handleSubmitFeedback} 
                    disabled={!feedbackText.trim() || !sessionId}
                  >
                    Submit Feedback
                  </Button>
                </CardFooter>
              </Card>
            </TabsContent>
            
            <TabsContent value="kb-info">
              <Card>
                <CardHeader>
                  <CardTitle>Knowledge Base Information</CardTitle>
                  <CardDescription>
                    Understanding how the AI uses structured knowledge to assist you
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    <div>
                      <h3 className="text-lg font-medium">XLSX Knowledge Sources</h3>
                      <p className="text-sm text-muted-foreground mb-4">
                        The AI assistant is powered by a structured knowledge base derived from these XLSX sheets:
                      </p>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="border rounded-md p-4">
                          <div className="flex items-center mb-2">
                            <span className="xlsx-badge xlsx-badge-problems">Problems.xlsx</span>
                            <span className="text-xs text-muted-foreground ml-2">Last updated: 2023-12-15</span>
                          </div>
                          <p className="text-sm">Defines mental health problems with descriptions and categories.</p>
                        </div>
                        
                        <div className="border rounded-md p-4">
                          <div className="flex items-center mb-2">
                            <span className="xlsx-badge xlsx-badge-assessment">SelfAssessment.xlsx</span>
                            <span className="text-xs text-muted-foreground ml-2">Last updated: 2023-12-15</span>
                          </div>
                          <p className="text-sm">Contains assessment questions linked to specific problems.</p>
                        </div>
                        
                        <div className="border rounded-md p-4">
                          <div className="flex items-center mb-2">
                            <span className="xlsx-badge xlsx-badge-suggestions">Suggestions.xlsx</span>
                            <span className="text-xs text-muted-foreground ml-2">Last updated: 2023-12-15</span>
                          </div>
                          <p className="text-sm">Provides coping mechanisms and resources for each problem.</p>
                        </div>
                        
                        <div className="border rounded-md p-4">
                          <div className="flex items-center mb-2">
                            <span className="xlsx-badge xlsx-badge-feedback">FeedbackPrompts.xlsx</span>
                            <span className="text-xs text-muted-foreground ml-2">Last updated: 2023-12-15</span>
                          </div>
                          <p className="text-sm">Guides the feedback collection process to improve AI responses.</p>
                        </div>
                        
                        <div className="border rounded-md p-4">
                          <div className="flex items-center mb-2">
                            <span className="xlsx-badge xlsx-badge-actions">NextActions.xlsx</span>
                            <span className="text-xs text-muted-foreground ml-2">Last updated: 2023-12-15</span>
                          </div>
                          <p className="text-sm">Defines conversation flow and follow-up actions.</p>
                        </div>
                        
                        <div className="border rounded-md p-4">
                          <div className="flex items-center mb-2">
                            <span className="xlsx-badge xlsx-badge-finetuning">FinetuningExamples.xlsx</span>
                            <span className="text-xs text-muted-foreground ml-2">Last updated: 2023-12-15</span>
                          </div>
                          <p className="text-sm">Shapes the AI's conversational style and response patterns.</p>
                        </div>
                      </div>
                    </div>
                    
                    <Separator />
                    
                    <div>
                      <h3 className="text-lg font-medium">How RAG Works</h3>
                      <p className="text-sm text-muted-foreground mb-4">
                        Retrieval-Augmented Generation (RAG) enhances the AI's responses by retrieving relevant information from the knowledge base.
                      </p>
                      
                      <ol className="list-decimal list-inside space-y-2 text-sm">
                        <li>Your message is analyzed to understand your needs</li>
                        <li>Relevant information is retrieved from the XLSX-derived knowledge base</li>
                        <li>The AI generates a response that incorporates this knowledge</li>
                        <li>Your feedback helps improve future responses</li>
                      </ol>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}