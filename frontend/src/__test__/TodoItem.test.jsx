import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { expect, vi } from 'vitest'
import TodoItem from './TodoItem.jsx'

const baseTodo = {
  id: 1,
  title: 'Sample Todo',
  done: false,
  comments: [],
};

describe('TodoItem', () => {
  it('renders with no comments correctly', () => {
    render(<TodoItem todo={baseTodo} />);
    expect(screen.getByText('Sample Todo')).toBeInTheDocument();
    expect(screen.getByText('No comments')).toBeInTheDocument();
  });

  it('renders with comments correctly', () => {
    const todoWithComment = {
      ...baseTodo,
      comments: [
        { id: 1, message: 'First comment' },
        { id: 2, message: 'Another comment' },
      ],
    };

    render(<TodoItem todo={todoWithComment} />);

    expect(screen.getByText('Sample Todo')).toBeInTheDocument();
    expect(screen.getByText('First comment')).toBeInTheDocument();
    expect(screen.getByText('Another comment')).toBeInTheDocument();

    // สำคัญมาก
    expect(screen.queryByText('No comments')).not.toBeInTheDocument();

    // ตรวจจำนวน comment (ถ้ามีเลข 2 แสดง)
    expect(screen.getByText(/2/)).toBeInTheDocument();
  });

  it('does not show no comments message when it has a comment', () => {
    const todoWithComment = {
      ...baseTodo,
      comments: [{ id: 1, message: 'First comment' }],
    };

    render(<TodoItem todo={todoWithComment} />);
    expect(screen.queryByText('No comments')).not.toBeInTheDocument();
  });
  it('makes callback to toggleDone when Toggle button is clicked', () => {
    const onToggleDone = vi.fn();
    render(
      <TodoItem 
       todo={baseTodo} 
       toggleDone={onToggleDone} />
    );
    const button = screen.getByRole('button', { name: /toggle/i });
    button.click();
    expect(onToggleDone).toHaveBeenCalledWith(baseTodo.id);
  });
  it('makes callback to deleteTodo when delete button is clicked', async () => {
    const mockDeleteTodo = vi.fn();
  
    render(
      <TodoItem
        todo={baseTodo}
        toggleDone={vi.fn()}
        deleteTodo={mockDeleteTodo}
        addNewComment={vi.fn()}
      />
    );
  
    const deleteButton = screen.getByText('❌');
    await userEvent.click(deleteButton);
  
    expect(mockDeleteTodo).toHaveBeenCalledTimes(1);
    expect(mockDeleteTodo).toHaveBeenCalledWith(1);
  });
  it('makes callback to addNewComment when a new comment is added', async () => {
    const onAddNewComment = vi.fn();
  
    render(
      <TodoItem
        todo={baseTodo}
        toggleDone={vi.fn()}
        deleteTodo={vi.fn()}
        addNewComment={onAddNewComment}
      />
    );

    const input = screen.getByRole('textbox');
    await userEvent.type(input, 'New comment');

    const button = screen.getByRole('button', { name: /add/i });
    await userEvent.click(button);

    expect(onAddNewComment).toHaveBeenCalledWith(baseTodo.id, 'New comment');
  });
  
});