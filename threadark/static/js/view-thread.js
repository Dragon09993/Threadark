console.log('view-thread.js loaded successfully');

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing thread features...');
    // Initialize 4chan-style features
    initializeThreadFeatures();
    
    const quoteLinks = document.querySelectorAll('.quotelink');

    quoteLinks.forEach(link => {
        link.addEventListener('mouseover', (event) => {
            const messageId = event.target.getAttribute('href').substring(2);
            const message = document.querySelector(`.message[data-message-no="${messageId}"]`);
            if (message) {
                message.classList.add('highlight');
            }
        });

        link.addEventListener('mouseout', (event) => {
            const messageId = event.target.getAttribute('href').substring(2);
            const message = document.querySelector(`.message[data-message-no="${messageId}"]`);
            if (message) {
                message.classList.remove('highlight');
            }
        });
    });
});

function initializeThreadFeatures() {
    console.log('Initializing thread features...');
    
    // Get the OP post number (first post on the page)
    const firstPost = document.querySelector('.message');
    if (!firstPost) {
        console.log('No posts found with .message class');
        return;
    }
    
    const opPostNo = firstPost.getAttribute('data-message-no');
    if (!opPostNo) {
        console.log('No data-message-no attribute found on first post');
        return;
    }
    
    console.log('OP post number:', opPostNo);
    
    // Process all posts for OP marking and reply tracking
    markOPReferences(opPostNo);
    addReplyIndicators();
    
    console.log('Thread features initialized successfully');
}

function markOPReferences(opPostNo) {
    // Find all message content paragraphs
    const messageParagraphs = document.querySelectorAll('.message .subtitle.is-6:last-child');
    
    messageParagraphs.forEach(paragraph => {
        if (paragraph.innerHTML) {
            // Look for >>postno patterns and mark OP references
            // Handle both &gt;&gt; (HTML encoded) and >> (plain text)
            let content = paragraph.innerHTML;
            
            // Replace &gt;&gt;postno with &gt;&gt;postno (OP) when postno matches OP
            const regexEncoded = new RegExp(`(&gt;&gt;${opPostNo})(?!\\s*\\(OP\\))(?=\\s|$|<|&)`, 'g');
            content = content.replace(regexEncoded, `$1 <span class="op-indicator">(OP)</span>`);
            
            // Replace >>postno with >>postno (OP) when postno matches OP
            const regexPlain = new RegExp(`(>>${opPostNo})(?!\\s*\\(OP\\))(?=\\s|$|<)`, 'g');
            content = content.replace(regexPlain, `$1 <span class="op-indicator">(OP)</span>`);
            
            paragraph.innerHTML = content;
        }
    });
}

function addReplyIndicators() {
    const posts = document.querySelectorAll('.message');
    const replyMap = new Map(); // postNo -> array of posts that reply to it
    
    // First pass: collect all reply relationships
    posts.forEach(post => {
        const postNo = post.getAttribute('data-message-no');
        const contentParagraph = post.querySelector('.subtitle.is-6:last-child');
        
        if (contentParagraph && contentParagraph.innerHTML) {
            const content = contentParagraph.innerHTML;
            
            // Find all post references in this message
            const referencesEncoded = content.match(/&gt;&gt;(\d+)/g);
            const referencesPlain = content.match(/>>(\d+)/g);
            
            const allReferences = [];
            if (referencesEncoded) {
                referencesEncoded.forEach(ref => {
                    const refPostNo = ref.replace('&gt;&gt;', '');
                    allReferences.push(refPostNo);
                });
            }
            if (referencesPlain) {
                referencesPlain.forEach(ref => {
                    const refPostNo = ref.replace('>>', '');
                    allReferences.push(refPostNo);
                });
            }
            
            // Add this post as a reply to all referenced posts
            allReferences.forEach(refPostNo => {
                if (!replyMap.has(refPostNo)) {
                    replyMap.set(refPostNo, []);
                }
                replyMap.get(refPostNo).push(postNo);
            });
        }
    });
    
    // Second pass: add reply indicators to posts
    posts.forEach(post => {
        const postNo = post.getAttribute('data-message-no');
        const replies = replyMap.get(postNo);
        
        if (replies && replies.length > 0) {
            console.log(`Adding backlinks to post ${postNo}, replies:`, replies);
            // Find the post number span in the header
            const postHeader = post.querySelector('.subtitle.is-6');
            console.log(`Post ${postNo} - postHeader:`, postHeader);
            
            // Find the span that contains the post number (starts with "No.")
            let postNoSpan = null;
            if (postHeader) {
                const greySpans = postHeader.querySelectorAll('.has-text-grey');
                greySpans.forEach(span => {
                    if (span.textContent && span.textContent.trim().startsWith('No.')) {
                        postNoSpan = span;
                    }
                });
            }
            console.log(`Post ${postNo} - postNoSpan:`, postNoSpan, postNoSpan ? postNoSpan.textContent : 'null');
            
            if (postNoSpan) {
                // Create reply links directly after the post number
                const replyLinks = replies.map(replyPostNo => {
                    return `<a href="#p${replyPostNo}" class="reply-backlink" data-post-no="${replyPostNo}"> &lt;&lt;${replyPostNo}</a>`;
                }).join('');
                
                // Append reply links directly to the post number span
                postNoSpan.innerHTML += replyLinks;
                
                // Add click handlers for reply links
                postNoSpan.querySelectorAll('.reply-backlink').forEach(link => {
                    link.addEventListener('click', (e) => {
                        e.preventDefault();
                        const targetPostNo = link.getAttribute('data-post-no');
                        const targetPost = document.querySelector(`#p${targetPostNo}`);
                        if (targetPost) {
                            targetPost.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            targetPost.classList.add('highlight-reply');
                            setTimeout(() => {
                                targetPost.classList.remove('highlight-reply');
                            }, 2000);
                        }
                    });
                });
            }
        }
    });
}

