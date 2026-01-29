'use client';

import React, { useState, useEffect } from 'react';
import { ChatWindow } from '../../components/ChatWindow';
import { useAuth } from 'better-auth/react';
import { useRouter } from 'next/navigation';

const ChatPage: React.FC = () => {
  const { session, isPending } = useAuth();
  const router = useRouter();
  const [conversationId, setConversationId] = useState<string>('');

  useEffect(() => {
    if (!isPending && !session) {
      router.push('/auth/login');
    } else if (session) {
      // For now, we'll use a temporary conversation ID
      // In a real app, you'd either get this from the URL or create a new one
      setConversationId(`conv_${Date.now()}`);
    }
  }, [session, isPending, router]);

  if (isPending) {
    return (
      <div className="flex justify-center items-center h-screen">
        <p>Loading...</p>
      </div>
    );
  }

  if (!session) {
    return null; // Redirect happens in useEffect
  }

  return (
    <div className="container mx-auto px-4 py-8 h-screen flex flex-col">
      <h1 className="text-2xl font-bold mb-6">AI Chat Assistant</h1>

      <div className="flex-1 overflow-hidden">
        {conversationId ? (
          <ChatWindow conversationId={conversationId} />
        ) : (
          <div className="flex justify-center items-center h-full">
            <p>Setting up conversation...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatPage;