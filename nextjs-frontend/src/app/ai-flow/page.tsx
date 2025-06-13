'use client'

import { useCallback } from 'react'
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  MarkerType,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

// Define the initial nodes for the AI flow visualization
const initialNodes = [
  {
    id: '1',
    type: 'default',
    data: { 
      label: 'User Input',
      description: 'User sends a message or question to the AI assistant'
    },
    position: { x: 250, y: 0 },
    className: 'flow-node flow-node-user',
  },
  {
    id: '2',
    type: 'default',
    data: { 
      label: 'Natural Language Understanding',
      description: 'AI processes and understands the user\'s intent'
    },
    position: { x: 250, y: 100 },
    className: 'flow-node flow-node-ai',
  },
  {
    id: '3',
    type: 'default',
    data: { 
      label: 'Knowledge Retrieval (RAG)',
      description: 'System retrieves relevant information from XLSX-based knowledge base',
      kb: ['Problems.xlsx', 'SelfAssessment.xlsx', 'Suggestions.xlsx']
    },
    position: { x: 250, y: 200 },
    className: 'flow-node flow-node-kb',
  },
  {
    id: '4',
    type: 'default',
    data: { 
      label: 'AI Reasoning',
      description: 'AI processes retrieved knowledge and applies reasoning',
      kb: ['FinetuningExamples.xlsx', 'FeedbackPrompts.xlsx', 'NextActions.xlsx']
    },
    position: { x: 250, y: 300 },
    className: 'flow-node flow-node-ai',
  },
  {
    id: '5',
    type: 'default',
    data: { 
      label: 'Response Generation',
      description: 'AI generates a contextually relevant response'
    },
    position: { x: 250, y: 400 },
    className: 'flow-node flow-node-ai',
  },
  {
    id: '6',
    type: 'default',
    data: { 
      label: 'User Feedback',
      description: 'User provides feedback on the AI\'s response'
    },
    position: { x: 250, y: 500 },
    className: 'flow-node flow-node-user',
  },
  {
    id: '7',
    type: 'default',
    data: { 
      label: 'Feedback Processing',
      description: 'System processes feedback to improve future responses',
      kb: ['FeedbackPrompts.xlsx']
    },
    position: { x: 450, y: 400 },
    className: 'flow-node flow-node-kb',
  },
];

// Define the connections between nodes
const initialEdges = [
  { id: 'e1-2', source: '1', target: '2', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e2-3', source: '2', target: '3', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e3-4', source: '3', target: '4', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e4-5', source: '4', target: '5', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e5-6', source: '5', target: '6', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e6-7', source: '6', target: '7', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: 'e7-4', source: '7', target: '4', animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
];

// Custom node component to display KB sources
const CustomNode = ({ data }: { data: { label: string; description: string; kb?: string[] } }) => {
  return (
    <div className="custom-node">
      <div>{data.label}</div>
      {data.kb && (
        <div className="kb-sources">
          {data.kb.map((source, index) => {
            let badgeClass = 'xlsx-badge';
            if (source.includes('Problems')) badgeClass += ' xlsx-badge-problems';
            if (source.includes('Suggestions')) badgeClass += ' xlsx-badge-suggestions';
            if (source.includes('Assessment')) badgeClass += ' xlsx-badge-assessment';
            if (source.includes('Feedback')) badgeClass += ' xlsx-badge-feedback';
            if (source.includes('Actions')) badgeClass += ' xlsx-badge-actions';
            if (source.includes('Finetuning')) badgeClass += ' xlsx-badge-finetuning';
            
            return (
              <span key={index} className={badgeClass}>
                {source}
              </span>
            );
          })}
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
    (params: { source: string; target: string; sourceHandle?: string | null; targetHandle?: string | null }) => 
      setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  return (
    <div className="container py-6">
      <h1 className="text-3xl font-bold mb-6">AI Flow Visualization</h1>
      
      <Tabs defaultValue="flow">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="flow">Flow Diagram</TabsTrigger>
          <TabsTrigger value="explanation">KB Integration Explanation</TabsTrigger>
        </TabsList>
        
        <TabsContent value="flow">
          <Card>
            <CardHeader>
              <CardTitle>AI Processing Flow</CardTitle>
              <CardDescription>
                Visual representation of how the AI processes user input and generates responses
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flow-container">
                <ReactFlow
                  nodes={nodes}
                  edges={edges}
                  onNodesChange={onNodesChange}
                  onEdgesChange={onEdgesChange}
                  onConnect={onConnect}
                  fitView
                  attributionPosition="bottom-right"
                >
                  <Controls />
                  <MiniMap />
                  <Background variant="dots" gap={12} size={1} />
                </ReactFlow>
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