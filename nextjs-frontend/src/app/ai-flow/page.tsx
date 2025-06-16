'use client'

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { MessageSquare, Brain, Database, Users, FileText, Smile, ThumbsUp } from 'lucide-react';

export default function AIFlowPage() {
  return (
    <div className="container py-6">
      <h1 className="text-3xl font-bold mb-6">Mental Health AI Assistant Flow</h1>
      <p className="text-lg text-gray-700 mb-6">
        This visualization demonstrates how our AI system processes user inputs, leverages structured knowledge bases,
        and generates personalized mental health support responses.
      </p>

      <Tabs defaultValue="flow">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="flow">Interactive Flow Diagram</TabsTrigger>
          <TabsTrigger value="explanation">KB Integration Details</TabsTrigger>
        </TabsList>

        <TabsContent value="flow" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>AI System Flow</CardTitle>
              <CardDescription>
                Visualization of how user inputs are processed through our AI system
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="relative w-full h-[800px] bg-slate-50 rounded-lg p-4 overflow-hidden">
                {/* Main SVG container for the flow diagram */}
                <svg className="w-full h-full" viewBox="0 0 1000 800" preserveAspectRatio="xMidYMid meet">
                  {/* Main vertical line */}
                  <line 
                    x1="500" y1="50" 
                    x2="500" y2="750" 
                    stroke="#94a3b8" 
                    strokeWidth="4"
                    strokeDasharray="10,5"
                    className="animate-dashFlow"
                  />
                  
                  {/* Horizontal connectors with gradient */}
                  <line 
                    x1="500" y1="150" 
                    x2="450" y2="150" 
                    stroke="url(#blueGradient)" 
                    strokeWidth="3"
                    strokeDasharray="5,3"
                    className="animate-dashFlow"
                  />
                  <line 
                    x1="500" y1="300" 
                    x2="450" y2="300" 
                    stroke="url(#purpleGradient)" 
                    strokeWidth="3"
                    strokeDasharray="5,3"
                    className="animate-dashFlow"
                  />
                  <line 
                    x1="500" y1="450" 
                    x2="450" y2="450" 
                    stroke="url(#greenGradient)" 
                    strokeWidth="3"
                    strokeDasharray="5,3"
                    className="animate-dashFlow"
                  />
                  <line 
                    x1="500" y1="600" 
                    x2="450" y2="600" 
                    stroke="url(#orangeGradient)" 
                    strokeWidth="3"
                    strokeDasharray="5,3"
                    className="animate-dashFlow"
                  />
                  
                  {/* Gradient definitions */}
                  <defs>
                    <linearGradient id="blueGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#3b82f6" />
                      <stop offset="100%" stopColor="#93c5fd" />
                    </linearGradient>
                    <linearGradient id="purpleGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#8b5cf6" />
                      <stop offset="100%" stopColor="#c4b5fd" />
                    </linearGradient>
                    <linearGradient id="greenGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#10b981" />
                      <stop offset="100%" stopColor="#6ee7b7" />
                    </linearGradient>
                    <linearGradient id="orangeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#f59e0b" />
                      <stop offset="100%" stopColor="#fcd34d" />
                    </linearGradient>
                  </defs>
                  
                  {/* Node 1: User Input */}
                  <g transform="translate(300, 100)" className="animate-fadeInScale">
                    <foreignObject width="300" height="100">
                      <div className="bg-white p-4 rounded-lg shadow-lg border border-blue-200">
                        <div className="flex items-center gap-2 mb-2">
                          <MessageSquare className="text-blue-500" size={20} />
                          <h3 className="font-semibold text-blue-700">User Input</h3>
                        </div>
                        <p className="text-sm text-gray-600">User messages are processed and analyzed for intent, sentiment, and key topics</p>
                      </div>
                    </foreignObject>
                  </g>
                  
                  {/* Node 2: Knowledge Base */}
                  <g transform="translate(300, 250)" className="animate-fadeInScale">
                    <foreignObject width="300" height="100">
                      <div className="bg-white p-4 rounded-lg shadow-lg border border-purple-200">
                        <div className="flex items-center gap-2 mb-2">
                          <Database className="text-purple-500" size={20} />
                          <h3 className="font-semibold text-purple-700">Knowledge Base</h3>
                        </div>
                        <p className="text-sm text-gray-600">Structured mental health resources, coping strategies, and therapeutic techniques</p>
                      </div>
                    </foreignObject>
                  </g>
                  
                  {/* Node 3: AI Processing */}
                  <g transform="translate(300, 400)" className="animate-fadeInScale">
                    <foreignObject width="300" height="100">
                      <div className="bg-white p-4 rounded-lg shadow-lg border border-green-200">
                        <div className="flex items-center gap-2 mb-2">
                          <Brain className="text-green-500" size={20} />
                          <h3 className="font-semibold text-green-700">AI Processing</h3>
                        </div>
                        <p className="text-sm text-gray-600">Combines user context with knowledge base to generate personalized, empathetic responses</p>
                      </div>
                    </foreignObject>
                  </g>
                  
                  {/* Node 4: Response Generation */}
                  <g transform="translate(300, 550)" className="animate-fadeInScale">
                    <foreignObject width="300" height="100">
                      <div className="bg-white p-4 rounded-lg shadow-lg border border-orange-200">
                        <div className="flex items-center gap-2 mb-2">
                          <Smile className="text-orange-500" size={20} />
                          <h3 className="font-semibold text-orange-700">Response Generation</h3>
                        </div>
                        <p className="text-sm text-gray-600">Crafts supportive responses with appropriate tone, empathy, and helpful resources</p>
                      </div>
                    </foreignObject>
                  </g>
                  
                  {/* Knowledge Base Legend */}
                  <g transform="translate(550, 150)" className="animate-fadeInScale">
                    <foreignObject width="350" height="500">
                      <div className="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
                        <div className="flex items-center gap-2 mb-4">
                          <FileText className="text-gray-700" size={20} />
                          <h3 className="font-semibold text-gray-800">Knowledge Base Structure</h3>
                        </div>
                        
                        <div className="space-y-4">
                          <div className="p-3 bg-blue-50 rounded-md border border-blue-100">
                            <h4 className="font-medium text-blue-700 mb-2">Mental Health Resources</h4>
                            <p className="text-sm text-gray-600">Curated information about mental health conditions, symptoms, and management strategies</p>
                          </div>
                          
                          <div className="p-3 bg-purple-50 rounded-md border border-purple-100">
                            <h4 className="font-medium text-purple-700 mb-2">Coping Techniques</h4>
                            <p className="text-sm text-gray-600">Evidence-based strategies for managing stress, anxiety, depression, and other mental health challenges</p>
                          </div>
                          
                          <div className="p-3 bg-green-50 rounded-md border border-green-100">
                            <h4 className="font-medium text-green-700 mb-2">Support Resources</h4>
                            <p className="text-sm text-gray-600">Information about professional help, crisis lines, and community support options</p>
                          </div>
                          
                          <div className="p-3 bg-orange-50 rounded-md border border-orange-100">
                            <h4 className="font-medium text-orange-700 mb-2">Conversation Examples</h4>
                            <p className="text-sm text-gray-600">Sample dialogues demonstrating empathetic responses to various mental health concerns</p>
                          </div>
                        </div>
                      </div>
                    </foreignObject>
                  </g>
                </svg>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="explanation" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Knowledge Base Integration Details</CardTitle>
              <CardDescription>
                How our system leverages structured knowledge for mental health support
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold mb-2">Knowledge Base Structure</h3>
                  <p className="text-gray-700 mb-4">
                    Our mental health AI assistant is powered by a comprehensive knowledge base that contains structured information
                    about mental health topics, coping strategies, therapeutic techniques, and support resources.
                  </p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                      <h4 className="font-medium text-blue-700 mb-2 flex items-center gap-2">
                        <Database size={16} /> Primary Knowledge Sources
                      </h4>
                      <ul className="list-disc pl-5 text-sm text-gray-600 space-y-1">
                        <li><span className="xlsx-badge xlsx-badge-conditions">Conditions.xlsx</span> - Mental health conditions and symptoms</li>
                        <li><span className="xlsx-badge xlsx-badge-coping">CopingStrategies.xlsx</span> - Evidence-based coping techniques</li>
                        <li><span className="xlsx-badge xlsx-badge-resources">Resources.xlsx</span> - Professional and community support options</li>
                        <li><span className="xlsx-badge xlsx-badge-suggestions">Suggestions.xlsx</span> - Personalized recommendations</li>
                      </ul>
                    </div>
                    
                    <div className="bg-purple-50 p-4 rounded-lg border border-purple-100">
                      <h4 className="font-medium text-purple-700 mb-2 flex items-center gap-2">
                        <Brain size={16} /> AI Training Materials
                      </h4>
                      <ul className="list-disc pl-5 text-sm text-gray-600 space-y-1">
                        <li><span className="xlsx-badge xlsx-badge-finetuning">FinetuningExamples.xlsx</span> - Conversation examples for AI training</li>
                        <li><span className="xlsx-badge xlsx-badge-prompts">SystemPrompts.xlsx</span> - Guidance for AI response generation</li>
                        <li><span className="xlsx-badge xlsx-badge-evaluation">EvaluationCriteria.xlsx</span> - Quality metrics for responses</li>
                      </ul>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold mb-2">Knowledge Integration Process</h3>
                  <p className="text-gray-700 mb-4">
                    The system processes user inputs through several stages to generate personalized, empathetic responses:
                  </p>
                  
                  <ol className="list-decimal pl-5 text-gray-700 space-y-3">
                    <li>
                      <strong>Input Analysis:</strong> User messages are processed to identify intent, sentiment, and key topics.
                    </li>
                    <li>
                      <strong>Knowledge Retrieval:</strong> Relevant information is retrieved from the knowledge base based on the user's specific needs.
                    </li>
                    <li>
                      <strong>Context Integration:</strong> The system maintains conversation history to provide coherent, contextually appropriate responses.
                    </li>
                    <li>
                      <strong>Response Generation:</strong> AI combines retrieved knowledge with conversation context to craft supportive responses.
                    </li>
                    <li>
                      <strong>Quality Assurance:</strong> Responses are evaluated against criteria for empathy, accuracy, and helpfulness.
                    </li>
                  </ol>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold mb-2">Expanding the Knowledge Base</h3>
                  <p className="text-gray-700 mb-4">
                    Our knowledge base is continuously updated to improve the quality and relevance of AI responses:
                  </p>
                  
                  <ul className="list-disc pl-5 text-gray-700 space-y-2">
                    <li>Adding new entries to <span className="xlsx-badge xlsx-badge-conditions">Conditions.xlsx</span> expands the AI's understanding of mental health topics</li>
                    <li>Updating <span className="xlsx-badge xlsx-badge-coping">CopingStrategies.xlsx</span> provides more techniques for the AI to recommend</li>
                    <li>Adding new suggestions to <span className="xlsx-badge xlsx-badge-suggestions">Suggestions.xlsx</span> provides more resources for the AI to recommend</li>
                    <li>Expanding <span className="xlsx-badge xlsx-badge-finetuning">FinetuningExamples.xlsx</span> refines the AI's conversational style and empathy</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}