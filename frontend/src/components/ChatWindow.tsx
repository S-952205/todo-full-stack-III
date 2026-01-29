import React, { useEffect, useRef, useState } from 'react';
import { useAuth } from 'better-auth/react';

interface ChatWindowProps {
  conversationId: string;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({ conversationId }) => {
  const chatkitRef = useRef<HTMLDivElement>(null);
  const { session } = useAuth();
  const [status, setStatus] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    if (!chatkitRef.current || !session?.token) return;

    // Dynamically import and set up ChatKit
    const setupChatKit = async () => {
      // Add ChatKit script to the document head if not already present
      if (!document.querySelector('#chatkit-script')) {
        const script = document.createElement('script');
        script.id = 'chatkit-script';
        script.src = 'https://cdn.platform.openai.com/deployments/chatkit/chatkit.js';
        script.async = true;
        document.head.appendChild(script);

        script.onload = () => {
          initializeChatKit();
        };
      } else {
        // If script is already loaded, initialize immediately
        initializeChatKit();
      }
    };

    const initializeChatKit = () => {
      if (!chatkitRef.current || !session?.token) return;

      // Remove any existing ChatKit elements
      chatkitRef.current.innerHTML = '';
      setIsLoading(false);

      // Create the ChatKit custom element
      const chatkitElement = document.createElement('openai-chatkit');

      // Configure the ChatKit element with the API options
      chatkitElement.setOptions({
        api: {
          url: `${process.env.NEXT_PUBLIC_API_URL}/api/chat`,
          domainKey: 'local-dev',
        },
        initialThread: conversationId || null,
        startScreen: {
          greeting: 'Welcome to the AI Assistant! How can I help you today?',
          prompts: [
            { prompt: 'What can you help me with?' },
            { prompt: 'Tell me about the weather' },
            { prompt: 'How do I use this?' }
          ]
        },
        theme: {
          colorScheme: 'light',
          density: 'normal',
          radius: 'soft',
        },
        header: {
          title: {
            text: 'AI Assistant'
          }
        }
      });

      // Add event listeners for ChatKit events to provide real-time feedback
      chatkitElement.addEventListener('chatkit.response.start', () => {
        setStatus('AI assistant is thinking...');
      });

      chatkitElement.addEventListener('chatkit.thread.load.start', (event) => {
        const threadId = event.detail.threadId;
        setStatus(`Loading conversation: ${threadId}`);
      });

      chatkitElement.addEventListener('chatkit.thread.load.end', () => {
        setStatus(null);
      });

      chatkitElement.addEventListener('chatkit.response.end', () => {
        setStatus('Response completed');
        setTimeout(() => setStatus(null), 2000); // Clear status after 2 seconds
      });

      chatkitElement.addEventListener('chatkit.tool.start', (event) => {
        const toolName = event.detail?.toolName || 'a tool';
        setStatus(`Using ${toolName}...`);
      });

      chatkitElement.addEventListener('chatkit.tool.end', (event) => {
        const toolName = event.detail?.toolName || 'a tool';
        setStatus(`${toolName} completed`);
        setTimeout(() => setStatus(null), 1500); // Clear status after 1.5 seconds
      });

      chatkitElement.addEventListener('chatkit.error', (event) => {
        console.error('ChatKit error:', event.detail);
        setStatus(`Error: ${event.detail?.message || 'Something went wrong'}`);
      });

      // Append the ChatKit element to the container
      chatkitRef.current.appendChild(chatkitElement);
    };

    setupChatKit();
  }, [session, conversationId]);

  return (
    <div className="h-full flex flex-col">
      {/* Status indicator */}
      {status && (
        <div className="bg-blue-100 border border-blue-300 text-blue-700 px-4 py-2 rounded mb-2 flex items-center">
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-blue-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{status}</span>
        </div>
      )}

      <div ref={chatkitRef} className="flex-1" style={{ minHeight: '500px' }} />
    </div>
  );
};