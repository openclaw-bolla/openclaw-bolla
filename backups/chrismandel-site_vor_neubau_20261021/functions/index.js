// Auto-redirects first-time visitors from English-speaking countries to /en/.
// Remembers the choice in a cookie so it never fights a manual language switch.

const ENGLISH_COUNTRIES = new Set([
  'US', 'GB', 'IE', 'AU', 'NZ', 'CA', 'ZA', 'SG', 'PH',
  'NG', 'KE', 'GH', 'JM', 'TT', 'BZ', 'GY', 'BB', 'ZW'
]);

function withLangCookie(response, lang) {
  const headers = new Headers(response.headers);
  headers.append('Set-Cookie', `lang=${lang}; Max-Age=31536000; Path=/; SameSite=Lax`);
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

export async function onRequestGet(context) {
  const { request } = context;
  const url = new URL(request.url);

  // Explicit override, used by the DE language-switch link on /en/ pages.
  if (url.searchParams.get('force') === 'de') {
    const res = await context.next();
    return withLangCookie(res, 'de');
  }

  const cookieHeader = request.headers.get('Cookie') || '';
  const match = /(?:^|;\s*)lang=(de|en)/.exec(cookieHeader);

  if (match) {
    if (match[1] === 'en') {
      return withLangCookie(Response.redirect(`${url.origin}/en/`, 302), 'en');
    }
    return context.next();
  }

  const country = (request.cf && request.cf.country) || '';
  if (ENGLISH_COUNTRIES.has(country)) {
    return withLangCookie(Response.redirect(`${url.origin}/en/`, 302), 'en');
  }

  const res = await context.next();
  return withLangCookie(res, 'de');
}
