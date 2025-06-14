'use client';

import React from 'react';
import ReactFlow, { Background, Controls, MiniMap } from 'reactflow';
import 'reactflow/dist/style.css';

// Custom node icons as SVG components
const UserIcon = () => (
  <svg viewBox="0 0 24 24" className="w-6 h-6">
    <path fill="currentColor" d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
  </svg>
);

const ChatIcon = () => (
  <svg viewBox="0 0 24 24" className="w-6 h-6">
    <path fill="currentColor" d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
  </svg>
);

const DatabaseIcon = () => (
  <svg viewBox="0 0 24 24" className="w-6 h-6">
    <path fill="currentColor" d="M12 2C6.48 2 2 4.48 2 7.5v9C2 19.52 6.48 22 12 22s10-2.48 10-5.5v-9C22 4.48 17.52 2 12 2zm0 13c-3.86 0-7-1.34-7-3v-2c1.42 1.1 4.07 2 7 2s5.58-.9 7-2v2c0 1.66-3.14 3-7 3z"/>
  </svg>
);

const BrainIcon = () => (
  <svg viewBox="0 0 24 24" className="w-6 h-6">
    <path fill="currentColor" d="M13 3c3.88 0 7 3.12 7 7 0 2.05-.88 3.9-2.28 5.19l2.5 2.5c.39.39.39 1.02 0 1.41-.39.39-1.02.39-1.41 0l-2.5-2.5C14.9 18.12 13.05 19 11 19c-3.88 0-7-3.12-7-7 0-2.05.88-3.9 2.28-5.19L3.78 4.31c-.39-.39-.39-1.02 0-1.41.39-.39 1.02-.39 1.41 0l2.5 2.5C9.1 3.88 10.95 3 13 3zm0 2c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5z"/>
  </svg>
);

const DocumentIcon = () => (
  <svg viewBox="0 0 24 24" className="w-6 h-6">
    <path fill="currentColor" d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm2 14h-3v3h-2v-3H8v-2h3v-3h2v3h3v2z"/>
  </svg>
);

const FeedbackIcon = () => (
  <svg viewBox="0 0 24 24" className="w-6 h-6">
    <path fill="currentColor" d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
  </svg>
);

const AnalyticsIcon = () => (
  <svg viewBox="0 0 24 24" className="w-6 h-6">
    <path fill="currentColor" d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
  </svg>
);

// Custom node component
const CustomNode = ({ data }) => (
  <div className="bg-white rounded-lg shadow-lg p-4 border border-gray-200 min-w-[200px]">
    <div className={`flex items-center gap-3 ${data.color} p-2 rounded-md`}>
      <div className="text-white">{data.icon}</div>
      <div className="text-white font-semibold">{data.label}</div>
    </div>
    {data.description && (
      <div className="mt-2 text-sm text-gray-600">{data.description}</div>
    )}
  </div>
);

// Initial nodes configuration
const initialNodes = [
  {
    id: '1',
    type: 'custom',
    position: { x: 400, y: 0 },
    data: {
      label: 'User Input',
      icon: <UserIcon />,
      color: 'bg-blue-500',
      description: 'User initiates conversation with mental health concerns'
    }
  },
  {
    id: '2',
    type: 'custom',
    position: { x: 400, y: 100 },
    data: {
      label: 'NLU & Intent Recognition',
      icon: <ChatIcon />,
      color: 'bg-green-500',
      description: 'System analyzes user input to understand intent and emotions'
    }
  },
  {
    id: '3',
    type: 'custom',
    position: { x: 400, y: 200 },
    data: {
      label: 'Knowledge Retrieval (RAG)',
      icon: <DatabaseIcon />,
      color: 'bg-orange-500',
      description: 'Retrieves relevant mental health information from knowledge base'
    }
  },
  {
    id: '4',
    type: 'custom',
    position: { x: 400, y: 300 },
    data: {
      label: 'AI Reasoning & Contextualization',
      icon: <BrainIcon />,
      color: 'bg-indigo-500',
      description: 'AI processes information and personalizes response strategy'
    }
  },
  {
    id: '5',
    type: 'custom',
    position: { x: 400, y: 400 },
    data: {
      label: 'Response Generation',
      icon: <DocumentIcon />,
      color: 'bg-yellow-500',
      description: 'Creates empathetic and helpful response based on analysis'
    }
  },
  {
    id: '6',
    type: 'custom',
    position: { x: 400, y: 500 },
    data: {
      label: 'User Receives Response & Provides Feedback',
      icon: <FeedbackIcon />,
      color: 'bg-pink-500',
      description: 'User receives support and provides feedback on helpfulness'
    }
  },
  {
    id: '7',
    type: 'custom',
    position: { x: 400, y: 600 },
    data: {
      label: 'Feedback Processing & Learning',
      icon: <AnalyticsIcon />,
      color: 'bg-purple-500',
      description: 'System learns from user feedback to improve future responses'
    }
  }
];



// Initial edges configuration
const initialEdges = [
  { 
    id: 'e1-2', 
    source: '1', 
    target: '2', 
    animated: true,
    style: {
      stroke: '#b1b1b7',
      strokeWidth: 2,
      filter: 'drop-shadow(0 2px 2px rgb(0 0 0 / 0.1))',
      transition: 'all 0.3s ease',
      animation: 'flowPathAnimation 1.5s infinite'
    },
    labelBgStyle: { fill: '#ffffff', rx: 4, ry: 4 },
    labelStyle: { fill: '#374151', fontSize: 12 },
    markerEnd: {
      type: 'arrowclosed',
      width: 20,
      height: 20,
      color: '#b1b1b7'
    }
  },
  { 
    id: 'e2-3', 
    source: '2', 
    target: '3', 
    animated: true,
    style: {
      stroke: '#b1b1b7',
      strokeWidth: 2,
      filter: 'drop-shadow(0 2px 2px rgb(0 0 0 / 0.1))',
      transition: 'all 0.3s ease',
      animation: 'flowPathAnimation 1.5s infinite'
    },
    labelBgStyle: { fill: '#ffffff', rx: 4, ry: 4 },
    labelStyle: { fill: '#374151', fontSize: 12 },
    markerEnd: {
      type: 'arrowclosed',
      width: 20,
      height: 20,
      color: '#b1b1b7'
    }
  },
  { 
    id: 'e3-4', 
    source: '3', 
    target: '4', 
    animated: true,
    style: {
      stroke: '#b1b1b7',
      strokeWidth: 2,
      filter: 'drop-shadow(0 2px 2px rgb(0 0 0 / 0.1))',
      transition: 'all 0.3s ease',
      animation: 'flowPathAnimation 1.5s infinite'
    },
    labelBgStyle: { fill: '#ffffff', rx: 4, ry: 4 },
    labelStyle: { fill: '#374151', fontSize: 12 },
    markerEnd: {
      type: 'arrowclosed',
      width: 20,
      height: 20,
      color: '#b1b1b7'
    }
  },
  { 
    id: 'e4-5', 
    source: '4', 
    target: '5', 
    animated: true,
    style: {
      stroke: '#b1b1b7',
      strokeWidth: 2,
      filter: 'drop-shadow(0 2px 2px rgb(0 0 0 / 0.1))',
      transition: 'all 0.3s ease',
      animation: 'flowPathAnimation 1.5s infinite'
    },
    labelBgStyle: { fill: '#ffffff', rx: 4, ry: 4 },
    labelStyle: { fill: '#374151', fontSize: 12 },
    markerEnd: {
      type: 'arrowclosed',
      width: 20,
      height: 20,
      color: '#b1b1b7'
    }
  },
  { 
    id: 'e5-6', 
    source: '5', 
    target: '6', 
    animated: true,
    style: {
      stroke: '#b1b1b7',
      strokeWidth: 2,
      filter: 'drop-shadow(0 2px 2px rgb(0 0 0 / 0.1))',
      transition: 'all 0.3s ease',
      animation: 'flowPathAnimation 1.5s infinite'
    },
    labelBgStyle: { fill: '#ffffff', rx: 4, ry: 4 },
    labelStyle: { fill: '#374151', fontSize: 12 },
    markerEnd: {
      type: 'arrowclosed',
      width: 20,
      height: 20,
      color: '#b1b1b7'
    }
  },
  { 
    id: 'e6-7', 
    source: '6', 
    target: '7', 
    animated: true,
    style: {
      stroke: '#b1b1b7',
      strokeWidth: 2,
      filter: 'drop-shadow(0 2px 2px rgb(0 0 0 / 0.1))',
      transition: 'all 0.3s ease',
      animation: 'flowPathAnimation 1.5s infinite'
    },
    labelBgStyle: { fill: '#ffffff', rx: 4, ry: 4 },
    labelStyle: { fill: '#374151', fontSize: 12 },
    markerEnd: {
      type: 'arrowclosed',
      width: 20,
      height: 20,
      color: '#b1b1b7'
    }
  }
];

// Knowledge base source badges with color coding
const KnowledgeBaseLegend = () => (
  <div className="absolute top-4 right-4 bg-white p-4 rounded-lg shadow-lg">
    <h3 className="text-lg font-semibold mb-2">Knowledge Base Sources</h3>
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <div className="w-4 h-4 rounded-full bg-blue-500"></div>
        <span>Problems</span>
      </div>
      <div className="flex items-center gap-2">
        <div className="w-4 h-4 rounded-full bg-green-500"></div>
        <span>Assessment</span>
      </div>
      <div className="flex items-center gap-2">
        <div className="w-4 h-4 rounded-full bg-orange-500"></div>
        <span>Suggestions</span>
      </div>
      <div className="flex items-center gap-2">
        <div className="w-4 h-4 rounded-full bg-indigo-500"></div>
        <span>Finetuning</span>
      </div>
      <div className="flex items-center gap-2">
        <div className="w-4 h-4 rounded-full bg-yellow-500"></div>
        <span>Actions</span>
      </div>
      <div className="flex items-center gap-2">
        <div className="w-4 h-4 rounded-full bg-pink-500"></div>
        <span>Feedback</span>
      </div>
    </div>
  </div>
);

// Define custom styles for the flow
const flowStyles = {
  background: '#f8fafc',
  width: '100%',
  height: '100vh'
};

// Main component
export default function AIFlowPage() {
  const [nodes, setNodes] = React.useState(initialNodes);
  const [edges, setEdges] = React.useState(initialEdges);

  return (
    <div style={flowStyles}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={{ custom: CustomNode }}
        className="bg-slate-50"
        style={{ width: '100%', height: '100vh' }}
        fitView
      >
        <Controls />
        <MiniMap />
        <Background color="#aaa" gap={16} />
        <KnowledgeBaseLegend />
      </ReactFlow>
    </div>
  );
}