from pathlib import Path

p = Path.home() / "Desktop/cbm/src/index.js"
s = p.read_text()

# Replace the existing price calculation with a normal per-card price.
old = '''        let priceCents = priceToCents(
          frontmatter.price
        );

        // Rosary Card uses quantity-based bundle pricing.
        if (slug === "rosary-card") {
          const rosaryPrice = getRosaryPrice(quantity);

          if (rosaryPrice <= 0) {
            throw new Error(
              `"${title}" is not available for checkout.`
            );
          }

          priceCents = Math.round(rosaryPrice * 100);
        }'''

new = '''        const priceCents = priceToCents(
          frontmatter.price
        );'''

if old in s:
    s = s.replace(old, new)

# If the Rosary function was added by the previous command, remove it.
start = s.find("function getRosaryPrice(quantity) {")
if start != -1:
    end = s.find("function priceToCents(rawPrice) {", start)
    if end == -1:
        raise SystemExit("Could not find priceToCents().")
    s = s[:start] + s[end:]

p.write_text(s)

print("Worker restored to normal per-card pricing:", p)
