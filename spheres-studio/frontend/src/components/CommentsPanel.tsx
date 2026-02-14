/**
 * SPHERES Studio — Comments Panel
 *
 * Threaded comment section with replies, markdown-lite formatting,
 * delete-own, and empty state.
 */

import { useCallback, useEffect, useState, type FormEvent } from 'react';
import { useAuth } from '../context/AuthContext';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface CommentData {
  id: string;
  design_id: string;
  user_id: string;
  user_name: string;
  parent_id: string | null;
  content: string;
  created_at: string;
  updated_at: string;
  replies: CommentData[];
}

interface CommentsPanelProps {
  designId: string;
  isOpen: boolean;
  onClose: () => void;
  onOpenAuth?: () => void;
}

// ---------------------------------------------------------------------------
// Markdown-lite renderer
// ---------------------------------------------------------------------------

/**
 * Renders a minimal subset of Markdown:
 *   **bold**  →  <strong>
 *   *italic*  →  <em>
 *   [text](url) → <a>
 *   `code`    → <code>
 */
function renderMarkdownLite(text: string): string {
  let html = text
    // Escape HTML entities
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  // Links: [text](url)
  html = html.replace(
    /\[([^\]]+)\]\(([^)]+)\)/g,
    '<a href="$2" target="_blank" rel="noopener noreferrer" style="color:#8B5CF6;text-decoration:underline">$1</a>',
  );

  // Bold: **text**
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  // Italic: *text*  (but not inside bold markers)
  html = html.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>');

  // Inline code: `code`
  html = html.replace(
    /`([^`]+)`/g,
    '<code style="background:#1F2937;padding:1px 4px;border-radius:3px;font-size:0.9em">$1</code>',
  );

  // Line breaks
  html = html.replace(/\n/g, '<br/>');

  return html;
}

// ---------------------------------------------------------------------------
// Helper: relative time
// ---------------------------------------------------------------------------

function timeAgo(dateStr: string): string {
  const seconds = Math.floor(
    (Date.now() - new Date(dateStr).getTime()) / 1000,
  );
  if (seconds < 60) return 'just now';
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 30) return `${days}d ago`;
  const months = Math.floor(days / 30);
  return `${months}mo ago`;
}

// ---------------------------------------------------------------------------
// Single comment component
// ---------------------------------------------------------------------------

function CommentItem({
  comment,
  depth,
  currentUserId,
  onReply,
  onDelete,
}: {
  comment: CommentData;
  depth: number;
  currentUserId: string | null;
  onReply: (parentId: string) => void;
  onDelete: (commentId: string) => void;
}) {
  const isOwn = currentUserId === comment.user_id;
  const maxDepth = 3;

  return (
    <div
      style={{
        ...styles.commentItem,
        marginLeft: Math.min(depth, maxDepth) * 20,
        borderLeft:
          depth > 0 ? '2px solid #374151' : 'none',
        paddingLeft: depth > 0 ? 12 : 0,
      }}
    >
      <div style={styles.commentHeader}>
        <div style={styles.commentAvatar}>
          {comment.user_name.charAt(0).toUpperCase()}
        </div>
        <span style={styles.commentAuthor}>{comment.user_name}</span>
        <span style={styles.commentTime}>{timeAgo(comment.created_at)}</span>
        {isOwn && (
          <button
            style={styles.deleteBtn}
            onClick={() => onDelete(comment.id)}
            title="Delete comment"
          >
            Delete
          </button>
        )}
      </div>

      <div
        style={styles.commentContent}
        dangerouslySetInnerHTML={{
          __html: renderMarkdownLite(comment.content),
        }}
      />

      <button
        style={styles.replyBtn}
        onClick={() => onReply(comment.id)}
      >
        Reply
      </button>

      {/* Nested replies */}
      {comment.replies.map((reply) => (
        <CommentItem
          key={reply.id}
          comment={reply}
          depth={depth + 1}
          currentUserId={currentUserId}
          onReply={onReply}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export default function CommentsPanel({
  designId,
  isOpen,
  onClose,
  onOpenAuth,
}: CommentsPanelProps) {
  const { user, token, isAuthenticated } = useAuth();

  const [comments, setComments] = useState<CommentData[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [content, setContent] = useState('');
  const [replyingTo, setReplyingTo] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // ----- Fetch comments -----
  const fetchComments = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/designs/${designId}/comments`);
      if (res.ok) {
        const data: CommentData[] = await res.json();
        setComments(data);
      }
    } catch {
      setError('Failed to load comments');
    } finally {
      setLoading(false);
    }
  }, [designId]);

  useEffect(() => {
    if (isOpen) {
      fetchComments();
    }
  }, [isOpen, fetchComments]);

  // Close on Escape
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [isOpen, onClose]);

  // ----- Submit comment -----
  const handleSubmit = useCallback(
    async (e: FormEvent) => {
      e.preventDefault();
      if (!isAuthenticated || !token) {
        onOpenAuth?.();
        return;
      }
      if (!content.trim()) return;

      setSubmitting(true);
      setError(null);
      try {
        const body: Record<string, string | null> = {
          content: content.trim(),
          parent_id: replyingTo,
        };
        const res = await fetch(`/api/designs/${designId}/comments`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(body),
        });
        if (!res.ok) {
          const data = await res.json();
          throw new Error(data.detail || 'Failed to post comment');
        }
        setContent('');
        setReplyingTo(null);
        await fetchComments();
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to post comment');
      } finally {
        setSubmitting(false);
      }
    },
    [content, replyingTo, token, isAuthenticated, designId, fetchComments, onOpenAuth],
  );

  // ----- Delete comment -----
  const handleDelete = useCallback(
    async (commentId: string) => {
      if (!token) return;
      try {
        const res = await fetch(`/api/comments/${commentId}`, {
          method: 'DELETE',
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok || res.status === 204) {
          await fetchComments();
        }
      } catch {
        setError('Failed to delete comment');
      }
    },
    [token, fetchComments],
  );

  // ----- Reply -----
  const handleReply = useCallback((parentId: string) => {
    setReplyingTo(parentId);
  }, []);

  const cancelReply = useCallback(() => {
    setReplyingTo(null);
  }, []);

  // Find the parent comment's author name for display
  const replyingToName = (() => {
    if (!replyingTo) return null;
    const findComment = (list: CommentData[]): string | null => {
      for (const c of list) {
        if (c.id === replyingTo) return c.user_name;
        const found = findComment(c.replies);
        if (found) return found;
      }
      return null;
    };
    return findComment(comments);
  })();

  // Count total comments (including nested)
  const countAll = (list: CommentData[]): number => {
    let n = 0;
    for (const c of list) {
      n += 1 + countAll(c.replies);
    }
    return n;
  };
  const totalCount = countAll(comments);

  if (!isOpen) return null;

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.panel} onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div style={styles.header}>
          <h2 style={styles.title}>
            Comments{' '}
            {totalCount > 0 && (
              <span style={styles.count}>({totalCount})</span>
            )}
          </h2>
          <button style={styles.closeBtn} onClick={onClose}>
            x
          </button>
        </div>

        {/* Error */}
        {error && <div style={styles.errorBox}>{error}</div>}

        {/* Comment list */}
        <div style={styles.commentList}>
          {loading && (
            <div style={styles.loadingRow}>
              <span style={styles.loadingText}>Loading comments...</span>
            </div>
          )}

          {!loading && comments.length === 0 && (
            <div style={styles.emptyState}>
              <p style={styles.emptyIcon}>...</p>
              <p style={styles.emptyTitle}>Be the first to share your thoughts</p>
              <p style={styles.emptyText}>
                Start a conversation about this activation design.
              </p>
            </div>
          )}

          {!loading &&
            comments.map((c) => (
              <CommentItem
                key={c.id}
                comment={c}
                depth={0}
                currentUserId={user?.id ?? null}
                onReply={handleReply}
                onDelete={handleDelete}
              />
            ))}
        </div>

        {/* Compose area */}
        <div style={styles.composeArea}>
          {replyingTo && (
            <div style={styles.replyingBar}>
              <span style={styles.replyingText}>
                Replying to <strong>{replyingToName || 'comment'}</strong>
              </span>
              <button style={styles.cancelReplyBtn} onClick={cancelReply}>
                Cancel
              </button>
            </div>
          )}

          {isAuthenticated ? (
            <form onSubmit={handleSubmit} style={styles.composeForm}>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Write a comment... (supports **bold**, *italic*, `code`, [links](url))"
                style={styles.composeTextarea}
                rows={3}
              />
              <div style={styles.composeActions}>
                <span style={styles.composeHint}>
                  Markdown-lite: **bold** *italic* `code` [link](url)
                </span>
                <button
                  type="submit"
                  style={{
                    ...styles.submitBtn,
                    opacity: submitting || !content.trim() ? 0.5 : 1,
                  }}
                  disabled={submitting || !content.trim()}
                >
                  {submitting ? 'Posting...' : 'Post Comment'}
                </button>
              </div>
            </form>
          ) : (
            <div style={styles.authPrompt}>
              <p style={styles.authPromptText}>
                Sign in to join the conversation
              </p>
              <button
                style={styles.authPromptBtn}
                onClick={() => onOpenAuth?.()}
              >
                Sign In
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Styles
// ---------------------------------------------------------------------------

const styles: Record<string, React.CSSProperties> = {
  overlay: {
    position: 'fixed',
    inset: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    backdropFilter: 'blur(4px)',
    display: 'flex',
    justifyContent: 'flex-end',
    zIndex: 9999,
  },
  panel: {
    width: '100%',
    maxWidth: 480,
    height: '100%',
    backgroundColor: '#111827',
    borderLeft: '1px solid #1F2937',
    display: 'flex',
    flexDirection: 'column' as const,
    fontFamily: 'Inter, system-ui, sans-serif',
    color: '#F9FAFB',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '16px 20px',
    borderBottom: '1px solid #1F2937',
  },
  title: {
    margin: 0,
    fontSize: 18,
    fontWeight: 700,
  },
  count: {
    fontWeight: 400,
    color: '#9CA3AF',
    fontSize: 15,
  },
  closeBtn: {
    background: 'none',
    border: 'none',
    color: '#6B7280',
    fontSize: 20,
    cursor: 'pointer',
    padding: 4,
  },
  errorBox: {
    margin: '12px 20px 0',
    backgroundColor: 'rgba(239, 68, 68, 0.15)',
    border: '1px solid rgba(239, 68, 68, 0.3)',
    borderRadius: 8,
    padding: '8px 12px',
    fontSize: 12,
    color: '#FCA5A5',
  },

  // Comment list
  commentList: {
    flex: 1,
    overflowY: 'auto' as const,
    padding: '16px 20px',
  },
  commentItem: {
    marginBottom: 16,
  },
  commentHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
    marginBottom: 4,
  },
  commentAvatar: {
    width: 24,
    height: 24,
    borderRadius: '50%',
    backgroundColor: '#6D28D9',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 12,
    fontWeight: 700,
    color: '#F9FAFB',
    flexShrink: 0,
  },
  commentAuthor: {
    fontSize: 13,
    fontWeight: 600,
    color: '#D1D5DB',
  },
  commentTime: {
    fontSize: 11,
    color: '#6B7280',
  },
  deleteBtn: {
    marginLeft: 'auto',
    background: 'none',
    border: 'none',
    color: '#EF4444',
    fontSize: 11,
    cursor: 'pointer',
    padding: '2px 6px',
    borderRadius: 4,
    opacity: 0.7,
  },
  commentContent: {
    fontSize: 14,
    lineHeight: 1.5,
    color: '#E5E7EB',
    marginLeft: 32,
  },
  replyBtn: {
    marginLeft: 32,
    marginTop: 4,
    background: 'none',
    border: 'none',
    color: '#6B7280',
    fontSize: 12,
    cursor: 'pointer',
    padding: '2px 0',
  },

  // Loading
  loadingRow: {
    display: 'flex',
    justifyContent: 'center',
    padding: 32,
  },
  loadingText: {
    fontSize: 14,
    color: '#6B7280',
  },

  // Empty state
  emptyState: {
    textAlign: 'center' as const,
    padding: '48px 16px',
  },
  emptyIcon: {
    fontSize: 36,
    margin: 0,
    color: '#374151',
    letterSpacing: 4,
  },
  emptyTitle: {
    fontSize: 16,
    fontWeight: 600,
    color: '#D1D5DB',
    margin: '12px 0 4px',
  },
  emptyText: {
    fontSize: 13,
    color: '#6B7280',
    margin: 0,
  },

  // Compose area
  composeArea: {
    borderTop: '1px solid #1F2937',
    padding: '12px 20px 16px',
  },
  replyingBar: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '6px 10px',
    marginBottom: 8,
    borderRadius: 6,
    backgroundColor: 'rgba(109, 40, 217, 0.1)',
    border: '1px solid rgba(109, 40, 217, 0.2)',
  },
  replyingText: {
    fontSize: 12,
    color: '#A78BFA',
  },
  cancelReplyBtn: {
    background: 'none',
    border: 'none',
    color: '#6B7280',
    fontSize: 12,
    cursor: 'pointer',
    padding: '2px 6px',
  },
  composeForm: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: 8,
  },
  composeTextarea: {
    width: '100%',
    padding: '10px 12px',
    borderRadius: 8,
    border: '1px solid #374151',
    backgroundColor: '#1F2937',
    color: '#F9FAFB',
    fontSize: 14,
    resize: 'vertical' as const,
    outline: 'none',
    fontFamily: 'Inter, system-ui, sans-serif',
    boxSizing: 'border-box' as const,
  },
  composeActions: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  composeHint: {
    fontSize: 11,
    color: '#4B5563',
  },
  submitBtn: {
    padding: '8px 16px',
    borderRadius: 8,
    border: 'none',
    backgroundColor: '#6D28D9',
    color: '#F9FAFB',
    fontSize: 13,
    fontWeight: 600,
    cursor: 'pointer',
  },

  // Auth prompt
  authPrompt: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '8px 0',
  },
  authPromptText: {
    margin: 0,
    fontSize: 13,
    color: '#9CA3AF',
  },
  authPromptBtn: {
    padding: '8px 16px',
    borderRadius: 8,
    border: 'none',
    backgroundColor: '#6D28D9',
    color: '#F9FAFB',
    fontSize: 13,
    fontWeight: 600,
    cursor: 'pointer',
  },
};
