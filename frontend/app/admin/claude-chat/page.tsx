'use client';

import { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function ClaudeChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: `👋 Hello! I'm Claude, your AI assistant for Project Athena. I can help you with:

🧠 **Understand**: Explain code, architecture, and how components work
📁 **Analyze**: Read files and provide detailed insights
🐛 **Debug**: Help troubleshoot issues and find solutions
✨ **Improve**: Suggest optimizations and best practices
📊 **Monitor**: Check project status and health
🚀 **Deploy**: Guide you through deployment steps

Ask me anything about your Project Athena system!`,
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/admin/claude-chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          conversationHistory: messages,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response from Claude');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}. Make sure the API is running.`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="max-w-4xl mx-auto p-4 h-screen flex flex-col">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="text-3xl">🧠</div>
            <h1 className="text-3xl font-bold text-white">Claude AI Assistant</h1>
          </div>
          <p className="text-purple-300">Admin-only chat interface for Project Athena</p>
        </div>

        {/* Chat Container */}
        <Card className="flex-1 flex flex-col bg-slate-800 border-purple-500/30 shadow-2xl">
          {/* Messages */}
          <CardContent className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-2xl rounded-lg p-4 ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : 'bg-slate-700 text-slate-100 rounded-bl-none'
                  }`}
                >
                  <p className="whitespace-pre-wrap text-sm leading-relaxed">
                    {message.content}
                  </p>
                  <span className="text-xs opacity-70 mt-2 block">
                    {message.timestamp.toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-slate-700 text-slate-100 rounded-lg rounded-bl-none p-4">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </CardContent>

          {/* Input Area */}
          <div className="border-t border-slate-700 p-6 bg-slate-800/50">
            <div className="flex gap-3">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask Claude anything about Project Athena..."
                disabled={loading}
                className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-400 focus:border-purple-500"
              />
              <Button
                onClick={handleSendMessage}
                disabled={loading || !input.trim()}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6"
              >
                {loading ? 'Thinking...' : 'Send'}
              </Button>
            </div>
            <p className="text-xs text-slate-400 mt-2">
              💡 Tip: Ask about code, architecture, status, debugging, or improvements
            </p>
          </div>
        </Card>

        {/* Quick Actions */}
        <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-3">
          <Button
            onClick={() => setInput('explain project athena')}
            variant="outline"
            className="bg-slate-800 border-purple-500/30 text-purple-300 hover:bg-slate-700"
          >
            📚 Explain Athena
          </Button>
          <Button
            onClick={() => setInput('status')}
            variant="outline"
            className="bg-slate-800 border-purple-500/30 text-purple-300 hover:bg-slate-700"
          >
            📊 Project Status
          </Button>
          <Button
            onClick={() => setInput('what agents do we have?')}
            variant="outline"
            className="bg-slate-800 border-purple-500/30 text-purple-300 hover:bg-slate-700"
          >
            🤖 Agents
          </Button>
          <Button
            onClick={() => setInput('api-health')}
            variant="outline"
            className="bg-slate-800 border-purple-500/30 text-purple-300 hover:bg-slate-700"
          >
            ⚡ API Health
          </Button>
        </div>
      </div>
    </div>
  );
}
