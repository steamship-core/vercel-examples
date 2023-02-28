import { ListGroup, Alert} from "flowbite-react";
import { useState } from "react";

export default function Documents({ dbId }: { dbId: string }) {

  const [books, setBooks] = useState<String[]|null>(null);

  const fetchBooks = async () => {
    const response = await fetch('/api/books', {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
        body: JSON.stringify({
          dbId: dbId,
        }),

    });

    const {books} = await response.json();
    setBooks(books)

  };

  if (!books) {
    fetchBooks()
  }

  return (
    <div>
    {(books && books.length !== 0) && (<div><p>Books read: </p>
    <ListGroup>

    {books && books.map((book) => (
       <ListGroup.Item key={book as string}>
📓 {book}
</ListGroup.Item>

  ))}
<ListGroup.Item key="more_books">
👋 Join our&nbsp;<a href="https://steamship.com/discord" className="font-semibold text-gray-900 underline dark:text-white decoration-sky-500">Discord</a>&nbsp;if you want to add more books
</ListGroup.Item>

  </ListGroup></div>
    )
}

{(books && books.length === 0) && (

<Alert
color="failure"
>
<span>
  <span className="font-medium">
    Index incomplete!
  </span>
  {' '}This index is not connected to a book. Please try to upload your book again <a href="https://www.steamship.com/build/ask-my-book-site" className="font-semibold text-gray-900 underline dark:text-white decoration-sky-500">here</a>.
  <br/>
  <br/>

  If this issue persists, please ping us on <a href="https://steamship.com/discord" className="font-semibold text-gray-900 underline dark:text-white decoration-sky-500">Discord</a>. We're happy to help. 
</span>
</Alert>

    
)}
  </div>
  );
}
