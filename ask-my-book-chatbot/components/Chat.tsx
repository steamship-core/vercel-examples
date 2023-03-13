import { useEffect, useState } from 'react'
import { Button } from './Button'
import { type Message, ChatLine, LoadingChatLine } from './ChatLine'
import { useCookies } from 'react-cookie'
import { HiOutlineArrowRight, HiOutlineRefresh, HiOutlinePlus } from 'react-icons/hi';
import LoadingDots from "./LoadingDots";

const COOKIE_NAME = 'ask-my-book-steamship'

// default first message to display in UI (not necessary to define the prompt)
export const initialMessages: Message[] = [
  {
    who: 'bot',
    message: 'Hi! I just read your book. Ask me a question about it!',
  },
]

const InputMessage = ({ input, setInput, sendMessage, loading }: any) => (
  <div className="mt-6 flex clear-both">
    <input
      type="text"
      aria-label="chat input"
      required
      className="min-w-0 flex-auto appearance-none rounded-md border border-zinc-900/10 bg-white px-3 py-[calc(theme(spacing.2)-1px)] shadow-md shadow-zinc-800/5 placeholder:text-zinc-400 focus:border-teal-500 focus:outline-none focus:ring-4 focus:ring-teal-500/10 sm:text-sm"
      value={input}
      onKeyDown={(e) => {
        if (e.key === 'Enter') {
          sendMessage(input)
          setInput('')
        }
      }}
      onChange={(e) => {
        setInput(e.target.value)
      }}
    />

    {!loading && (<Button
        type="submit"
        gradientDuoTone="greenToBlue"
        className="ml-2 flex-none"
        onClick={(e) => {
          sendMessage(input)
          setInput('')
        }}
      >
      <HiOutlineArrowRight className="h-5 w-5" />
      </Button>
      )}

      {loading && (
                  <Button
                  gradientDuoTone="greenToBlue"
                  className="ml-2 h-20"
                  disabled
                  >
                    <LoadingDots color="white" style="large" />
                  </Button>
                )}
  </div>
)

export function Chat({ baseUrl }: { baseUrl: string }) {
  const [messages, setMessages] = useState<Message[]>(initialMessages)
  const [input, setInput] = useState('')
  const [chatSessionId, setChatSessionId] = useState(Math.random().toString(36).substring(7))
  const [loading, setLoading] = useState(false)
  const [cookie, setCookie] = useCookies([COOKIE_NAME])
  const [error, setError] = useState<String | undefined>(undefined);


  useEffect(() => {
    if (!cookie[COOKIE_NAME]) {
      setCookie(COOKIE_NAME, Math.random().toString(36).substring(7))

    }
  }, [cookie, setCookie])

  const resetChatSessionId = () => {
    setChatSessionId(Math.random().toString(36).substring(7))
  }

  const resetChatConversation = () => {
    resetChatSessionId()
    setMessages(initialMessages)
  }

  const regenerateAnswer = () => {
    let {who: who_first} = messages[messages.length - 1]
    let offset = 0
    if (who_first === "bot") {
      offset = 1
    }
    const {message, who} = messages[messages.length - 1 - offset]
    sendMessage(message as string, messages.slice(0,messages.length-1 - offset))
  }


  const sendMessage = async (message: string, message_history?: Message[]) => {
    setLoading(true)
    setError(undefined);
    const newMessages = [
      ...message_history || messages,
      { message: message, who: 'user' } as Message,
    ]
    setMessages(newMessages)

    const response = await fetch(baseUrl + '/answer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question: message, 
        chat_session_id: chatSessionId,
      }),
      })
    if (!response.ok) {
      setLoading(false);
      setError(response.statusText);
      return;
    }

    const {answer, sources, is_plausible} = await response.json()
    setLoading(false);

    if (error) {
      setError(error)
    } else {
        setMessages((oldMessages) => [
          ...oldMessages,
          { message: answer.trim(), who: 'bot', sources: sources, isPlausible: is_plausible } as Message
        ])
    } 
  }


  return (
    <div>
    <div className="rounded-2xl border-zinc-100  lg:border lg:p-6">
      {messages.map(({ message, who, sources, isPlausible }, index) => (
        <ChatLine key={index} who={who} message={message} sources={sources} isPlausible={isPlausible} />
      ))}

      {loading && <LoadingChatLine />}

      {messages.length < 2 ? (
        <span className="mx-auto flex flex-grow text-gray-600 clear-both">
          Type a message to start the conversation
        </span>) : (<span className="justify-center content-center	mx-auto flex flex-grow clear-both">
        <Button  disabled={loading}   outline={true}
 onClick={regenerateAnswer} gradientDuoTone="greenToBlue">
  <div className="flex flex-row items-center">
          <HiOutlineRefresh className="mr-2 h-5 w-5" /> Regenerate response
          </div>
    </Button><Button  disabled={loading}   outline={true}
 onClick={resetChatConversation} gradientDuoTone="greenToBlue" className="ml-2">
  <div className="flex flex-row items-center">
          <HiOutlinePlus className="mr-2 h-5 w-5" /> New chat
          </div>
    </Button>
        </span>
      )}

      
      <InputMessage
        input={input}
        setInput={setInput}
        sendMessage={sendMessage}
        loading={loading}
      />

      { error && (
          <div className="rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p>{error}</p>
              </div>
            </div>
          </div>
      )}
    </div>
    </div>
  )
}
