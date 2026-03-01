from sap_discovery.models.schema import Reference

def build_refs(sources) -> list:
        """Convert source dicts to Reference objects."""
        references = []
        seen_urls = set()
        for source in sources:
            url = source.get("url", "").strip()
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            references.append(Reference(
                title=source.get("title", "").strip() or "Unknown",
                url=url,
                source_type="sap_docs" if source.get("source_type") == "sap_docs" else "web"
            ))
        return references