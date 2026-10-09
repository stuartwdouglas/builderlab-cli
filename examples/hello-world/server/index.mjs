const html = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Hello World</title>
    <style>
      :root { color-scheme: light; font-family: system-ui, sans-serif; }
      body { margin: 0; min-height: 100vh; display: grid; place-items: center; background: #f5f3ef; color: #202a24; }
      main { padding: 3rem 2rem; text-align: center; }
      h1 { font-size: clamp(3rem, 10vw, 6rem); letter-spacing: -0.06em; margin: 0 0 1rem; }
      p { font-size: 1.25rem; color: #5b665f; }
    </style>
  </head>
  <body>
    <main>
      <h1>Hello World</h1>
      <p>A tiny page to say hello.</p>
    </main>
  </body>
</html>`;

export default {
  fetch(request) {
    const path = new URL(request.url).pathname;
    if (path !== "/") {
      return new Response("Not found", { status: 404 });
    }
    return new Response(request.method === "HEAD" ? null : html, {
      headers: { "content-type": "text/html; charset=utf-8" },
    });
  },
};
