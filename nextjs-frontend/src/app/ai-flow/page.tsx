'use client'

import React, { useCallback } from 'react'
import type { Node, Edge, Connection, NodeProps } from 'reactflow';

// Define custom edge type with our additional properties
type CustomEdge = Edge & {
  label?: string;
  labelBgPadding?: [number, number];
  labelBgStyle?: {
    fill: string;
    fillOpacity: number;
    rx?: number;
    ry?: number;
  };
  labelStyle?: {
    fontSize: number;
    fill: string;
    fontWeight: number;
  };
};
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  MarkerType,
  applyNodeChanges,
  applyEdgeChanges,
  NodeChange,
  EdgeChange,
  BackgroundVariant
} from 'reactflow'
import 'reactflow/dist/style.css'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { MessageSquare, Brain, Database, Users, FileText, Smile, ThumbsUp } from 'lucide-react';

// Define the type for our custom node data
export interface CustomNodeData {
  label: string;
  description: string;
  icon: JSX.Element;
  details: string;
  kb?: string[]; // Knowledge base sources, optional
}

// Define AppNode type alias
export type AppNode = Node<CustomNodeData, string | undefined>;
export type AppEdge = Edge<any>;

// Define the initial nodes for the AI flow visualization
const initialNodes: AppNode[] = [
  {
    id: '1',
    type: 'custom',
    data: {
      label: 'User Input',
      description: 'User sends a message or question through the chat interface.',
      icon: <Users className="h-8 w-8 text-blue-500" />,
      details: 'The starting point of the AI interaction flow. User inputs can range from specific questions about mental health concerns to open-ended requests for support.'
    },
    position: { x: 250, y: 0 },
    className: 'shadow-lg rounded-lg border-2 border-blue-500 bg-white',
  },
  {
    id: '2',
    type: 'custom',
    data: {
      label: 'NLU & Intent Recognition',
      description: 'AI analyzes and understands the user\'s query intent.',
      icon: <MessageSquare className="h-8 w-8 text-purple-500" />,
      details: 'Natural Language Understanding processes the text to identify key topics, sentiment, and the underlying intent (e.g., seeking information, requesting help with a specific problem, or looking for coping strategies).'
    },
    position: { x: 250, y: 120 },
    className: 'shadow-lg rounded-lg border-2 border-purple-500 bg-white',
  },
  {
    id: '3',
    type: 'custom',
    data: {
      label: 'Knowledge Retrieval (RAG)',
      description: 'Retrieves relevant information from structured Knowledge Base.',
      icon: <Database className="h-8 w-8 text-green-500" />,
      kb: ['Problems.xlsx', 'SelfAssessment.xlsx', 'Suggestions.xlsx'],
      details: 'Using Retrieval-Augmented Generation (RAG), the system searches through the knowledge base to find information relevant to the user\'s query. This enhances the AI\'s responses with domain-specific knowledge about mental health.'
    },
    position: { x: 250, y: 240 },
    className: 'shadow-lg rounded-lg border-2 border-green-500 bg-white',
  },
  {
    id: '4',
    type: 'custom',
    data: {
      label: 'AI Reasoning & Contextualization',
      description: 'AI processes retrieved information and applies clinical reasoning.',
      icon: <Brain className="h-8 w-8 text-orange-500" />,
      kb: ['FinetuningExamples.xlsx', 'FeedbackPrompts.xlsx', 'NextActions.xlsx'],
      details: 'The AI combines the retrieved knowledge with conversation history to reason about the user\'s situation. It applies patterns learned from fine-tuning examples to ensure responses are clinically appropriate and empathetic.'
    },
    position: { x: 250, y: 360 },
    className: 'shadow-lg rounded-lg border-2 border-orange-500 bg-white',
  },
  {
    id: '5',
    type: 'custom',
    data: {
      label: 'Response Generation',
      description: 'AI crafts a personalized, empathetic response based on analysis.',
      icon: <FileText className="h-8 w-8 text-indigo-500" />,
      details: 'The system generates a response that addresses the user\'s needs, incorporating relevant information from the knowledge base while maintaining an empathetic tone appropriate for mental health support.'
    },
    position: { x: 250, y: 480 },
    className: 'shadow-lg rounded-lg border-2 border-indigo-500 bg-white',
  },
  {
    id: '6',
    type: 'custom',
    data: {
      label: 'User Receives Response & Provides Feedback',
      description: 'User reads the AI response and can provide explicit or implicit feedback.',
      icon: <Smile className="h-8 w-8 text-yellow-500" />,
      details: 'The user receives the AI\'s response and can react to it in various ways: asking follow-up questions, rating helpfulness, or providing specific feedback on the response quality.'
    },
    position: { x: 250, y: 600 },
    className: 'shadow-lg rounded-lg border-2 border-yellow-500 bg-white',
  },
  {
    id: '7',
    type: 'custom',
    data: {
      label: 'Feedback Processing & Learning',
      description: 'System analyzes feedback to improve future responses.',
      icon: <ThumbsUp className="h-8 w-8 text-pink-500" />,
      kb: ['FeedbackPrompts.xlsx'],
      details: 'User feedback is processed to continuously improve the AI. This includes updating response strategies, refining the knowledge base, and adjusting the conversation flow based on what has been most helpful to users.'
    },
    position: { x: 500, y: 480 }, // Adjusted position for better flow
    className: 'shadow-lg rounded-lg border-2 border-pink-500 bg-white',
  }
];

// Generate edges so every node is connected to every other node (excluding self-connections)
const nodeIds = initialNodes.map(node => node.id);
const initialEdges: CustomEdge[] = nodeIds.flatMap((sourceId, i) =>
  nodeIds.filter((targetId, j) => i !== j).map((targetId, j) => ({
    id: `e${sourceId}-${targetId}`,
    source: sourceId,
    target: targetId,
    animated: true,
    labelBgPadding: [12, 8] as [number, number],
    markerEnd: { type: MarkerType.ArrowClosed, color: '#4299e1', width: 20, height: 20 },
    label: `From ${sourceId} to ${targetId}`,
    labelBgStyle: { fill: '#EBF5FF', fillOpacity: 0.9 },
    labelStyle: { fontSize: 13, fill: '#2b6cb0', fontWeight: 700 },
  }))
);

// Define the connections between nodes with enhanced styling and descriptions
// Using thicker lines and enhanced styling to make edges look like flowing cables
// Define custom edge styles with enhanced connector-like appearance
const edgeGlowStyle = {
  filter: 'drop-shadow(0 0 3px rgba(255, 255, 255, 0.5))',
};

// Custom node component to display KB sources
interface CustomNodeProps extends NodeProps<CustomNodeData> {
  data: CustomNodeData;
}

const CustomNode: React.FC<CustomNodeProps> = ({ data }) => {
  return (
    <div className="p-4 rounded-md text-center hover:shadow-xl transition-shadow duration-300 bg-white bg-opacity-95">
      {data?.icon && <div className="flex justify-center mb-3">{data.icon}</div>}
      <div className="font-semibold mb-2 text-sm">{data.label}</div>
      <div className="text-xs text-gray-600 mb-3 px-2">{data.description}</div>

      {data.details && (
        <div className="mt-2 mb-3 px-2">
          <details className="text-xs text-left">
            <summary className="cursor-pointer font-medium text-blue-600 hover:text-blue-800">More details</summary>
            <p className="mt-2 text-gray-700 bg-gray-50 p-2 rounded">{data.details}</p>
          </details>
        </div>
      )}

      {data.kb && (
        <div className="mt-2 pt-2 border-t border-gray-200">
          <div className="text-xs font-medium text-gray-500 mb-2">Knowledge Base Sources:</div>
          <div className="flex flex-wrap justify-center gap-1">
            {data.kb?.map((source: string, index: number) => {
              let badgeColorClass = 'bg-slate-200 text-slate-700'; // Default
              let tooltipText = '';

              if (source.includes('Problems')) {
                badgeColorClass = 'bg-red-100 text-red-700 border border-red-300';
                tooltipText = 'Contains definitions and descriptions of mental health problems';
              }
              else if (source.includes('Assessment')) {
                badgeColorClass = 'bg-yellow-100 text-yellow-700 border border-yellow-300';
                tooltipText = 'Contains assessment questions to understand user situation';
              }
              else if (source.includes('Suggestions')) {
                badgeColorClass = 'bg-green-100 text-green-700 border border-green-300';
                tooltipText = 'Contains coping strategies and resources for recommendations';
              }
              else if (source.includes('Finetuning')) {
                badgeColorClass = 'bg-blue-100 text-blue-700 border border-blue-300';
                tooltipText = 'Examples that shape AI conversational style and empathy';
              }
              else if (source.includes('Actions')) {
                badgeColorClass = 'bg-indigo-100 text-indigo-700 border border-indigo-300';
                tooltipText = 'Guides on appropriate follow-up actions based on context';
              }
              else if (source.includes('Feedback')) {
                badgeColorClass = 'bg-pink-100 text-pink-700 border border-pink-300';
                tooltipText = 'Structures how feedback is collected and processed';
              }

              return (
                <div key={index} className="group relative inline-block">
                  <span
                    className={`px-2 py-0.5 rounded-full text-xs font-medium ${badgeColorClass} cursor-help`}
                  >
                    {source}
                  </span>
                  <div className="opacity-0 bg-black text-white text-xs rounded py-1 px-2 absolute z-10 bottom-full left-1/2 transform -translate-x-1/2 mb-1 group-hover:opacity-100 transition-opacity duration-300 w-48 text-center pointer-events-none">
                    {tooltipText}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

// Define the node types
const nodeTypes = {
  custom: CustomNode,
};

export default function AIFlowPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

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

        <TabsContent value="flow">
          <Card>
            <CardHeader>
              <CardTitle>AI Processing Flow</CardTitle>
              <CardDescription>
                Visual representation of how the AI processes user input and generates responses using knowledge bases
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
                <h3 className="text-sm font-medium text-blue-800 mb-2">How to use this diagram:</h3>
                <ul className="text-xs text-blue-700 list-disc pl-5 space-y-1">
                  <li>Hover over nodes to see detailed information</li>
                  <li>Click "More details" in each node to learn about that processing stage</li>
                  <li>Hover over KB Source badges to understand what each knowledge source provides</li>
                  <li>Follow the animated flow to understand the complete AI processing cycle</li>
                </ul>
              </div>

              <div className="flow-container h-[600px]">
                <ReactFlow
                  nodes={nodes}
                  edges={edges}
                  onNodesChange={onNodesChange}
                  onEdgesChange={onEdgesChange}
                  onConnect={onConnect}
                  nodeTypes={nodeTypes}
                  fitView
                  attributionPosition="bottom-right"
                  defaultEdgeOptions={{
                    // Enhanced cable-like appearance for all edges
                    style: {
                      stroke: '#5A67D8',
                      strokeWidth: 6,
                      filter: edgeGlowStyle.filter, // Use the defined glow style
                      transition: 'all 0.3s ease',
                      animation: 'flow 30s linear infinite',
                    },
                    animated: true,
                    labelBgPadding: [12, 8] as [number, number],
                    labelBgStyle: {
                      fill: '#FFFFFF',
                      fillOpacity: 0.95,
                      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                    },
                    labelStyle: {
                      fontSize: 13,
                      fontWeight: 700,
                      letterSpacing: '0.02em',
                    },
                    markerEnd: {
                      type: MarkerType.ArrowClosed,
                      width: 24,
                      height: 24,
                      strokeWidth: 2,
                    }
                  }}
                  // Add custom CSS for flowing animation
                  className="with-flowing-gradient"
                  style={{
                    background: 'radial-gradient(circle at center, rgba(255,255,255,0.1) 0%, transparent 70%)',
                  }}
                >
                  <Controls />
                  <MiniMap
                    // Enhanced MiniMap styling to better reflect the cable colors
                    nodeStrokeColor={(n: AppNode) => {
                      if (n.style?.borderColor) return n.style.borderColor as string;
                      if (n.style?.background) return n.style.background as string;
                      return '#000';
                    }}
                    nodeColor={(n: AppNode) => {
                      if (n.style?.background) return n.style.background as string;
                      return '#fff';
                    }}
                    // Style the edges in the MiniMap to match the main view
                    style={{ backgroundColor: '#f9fafb' }}
                    maskColor="rgba(240, 240, 240, 0.6)"
                  />
                  <Background variant={BackgroundVariant.Lines} gap={12} size={1} />
                </ReactFlow>
              </div>

              <div className="mt-6 p-4 bg-gray-50 rounded-md">
                <h3 className="text-sm font-medium mb-3">Knowledge Base Color Legend:</h3>
                <div className="flex flex-wrap gap-3">
                  <div className="flex items-center">
                    <span className="inline-block w-3 h-3 bg-red-100 border border-red-300 rounded-full mr-2"></span>
                    <span className="text-xs">Problems</span>
                  </div>
                  <div className="flex items-center">
                    <span className="inline-block w-3 h-3 bg-yellow-100 border border-yellow-300 rounded-full mr-2"></span>
                    <span className="text-xs">Assessment</span>
                  </div>
                  <div className="flex items-center">
                    <span className="inline-block w-3 h-3 bg-green-100 border border-green-300 rounded-full mr-2"></span>
                    <span className="text-xs">Suggestions</span>
                  </div>
                  <div className="flex items-center">
                    <span className="inline-block w-3 h-3 bg-blue-100 border border-blue-300 rounded-full mr-2"></span>
                    <span className="text-xs">Finetuning</span>
                  </div>
                  <div className="flex items-center">
                    <span className="inline-block w-3 h-3 bg-indigo-100 border border-indigo-300 rounded-full mr-2"></span>
                    <span className="text-xs">Actions</span>
                  </div>
                  <div className="flex items-center">
                    <span className="inline-block w-3 h-3 bg-pink-100 border border-pink-300 rounded-full mr-2"></span>
                    <span className="text-xs">Feedback</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="explanation">
          <Card>
            <CardHeader>
              <CardTitle>Knowledge Base Integration</CardTitle>
              <CardDescription>
                How the XLSX-based knowledge base enhances AI capabilities
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-medium">Knowledge Retrieval (RAG)</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    The AI uses Retrieval-Augmented Generation to pull relevant information from the knowledge base:
                  </p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="border rounded-md p-4">
                      <div className="flex items-center mb-2">
                        <span className="xlsx-badge xlsx-badge-problems">Problems.xlsx</span>
                      </div>
                      <p className="text-sm">Provides definitions and descriptions of mental health problems to help the AI identify user concerns.</p>
                    </div>

                    <div className="border rounded-md p-4">
                      <div className="flex items-center mb-2">
                        <span className="xlsx-badge xlsx-badge-assessment">SelfAssessment.xlsx</span>
                      </div>
                      <p className="text-sm">Supplies assessment questions that the AI can use to better understand the user's situation.</p>
                    </div>

                    <div className="border rounded-md p-4">
                      <div className="flex items-center mb-2">
                        <span className="xlsx-badge xlsx-badge-suggestions">Suggestions.xlsx</span>
                      </div>
                      <p className="text-sm">Contains coping strategies and resources that the AI can recommend based on identified problems.</p>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-medium">AI Reasoning</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    The AI's reasoning process is influenced by these knowledge sources:
                  </p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="border rounded-md p-4">
                      <div className="flex items-center mb-2">
                        <span className="xlsx-badge xlsx-badge-finetuning">FinetuningExamples.xlsx</span>
                      </div>
                      <p className="text-sm">Shapes the AI's conversational style, ensuring responses are empathetic and appropriate for mental health support.</p>
                    </div>

                    <div className="border rounded-md p-4">
                      <div className="flex items-center mb-2">
                        <span className="xlsx-badge xlsx-badge-actions">NextActions.xlsx</span>
                      </div>
                      <p className="text-sm">Guides the AI on appropriate follow-up actions based on the conversation context.</p>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-medium">Feedback Loop</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    User feedback is processed to continuously improve the AI:
                  </p>

                  <div className="border rounded-md p-4">
                    <div className="flex items-center mb-2">
                      <span className="xlsx-badge xlsx-badge-feedback">FeedbackPrompts.xlsx</span>
                    </div>
                    <p className="text-sm">Structures how feedback is collected and processed to enhance future AI responses.</p>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-medium">Impact of XLSX Updates</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    When the XLSX files are updated, the changes immediately impact the AI's capabilities:
                  </p>

                  <ul className="list-disc list-inside space-y-2 text-sm">
                    <li>Adding new problems to <span className="xlsx-badge xlsx-badge-problems">Problems.xlsx</span> expands the AI's ability to recognize and address more mental health concerns</li>
                    <li>Updating questions in <span className="xlsx-badge xlsx-badge-assessment">SelfAssessment.xlsx</span> improves the AI's assessment capabilities</li>
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