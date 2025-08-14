import re

def format_html_form(htmlStr: str):
    """
    ---
    Format a single-line HTML string with proper indentation and line breaks
    ---
    
    Parameters:
        htmlStr (str) - Single-line HTML string to format
    Returns:
        formatted (str) - Formatted HTML string with proper indentation
    """
    htmlStr = re.sub(r">\s+<", "><", htmlStr.strip())
    
    selfClosingTags = {"input", "br", "hr", "img", "meta", "link", "area", "base", "col", "embed", "source", "track", "wbr"}
    
    result = []
    indent_level = 0
    i = 0
    
    while i < len(htmlStr):
        if htmlStr[i] == "<":
            tagEnd = htmlStr.find(">", i)
            if tagEnd == -1:
                result.append(htmlStr[i:])
                break
            
            tag = htmlStr[i:tagEnd + 1]
            
            #Extract tag name and check if its closing ("</div>" -> set isClosing = False && assigns tagName = div)
            tagMatch = re.match(r"<(/?)(\w+)", tag)
            if tagMatch:
                isClosing = tagMatch.group(1) == "/"
                tagName= tagMatch.group(2).lower()
                is_self_closing = tag.endswith("/>") or tagName in selfClosingTags
                
                if isClosing:
                    indent_level -= 1
                
                if result:
                    result.append("\n")
                result.append("\t" * indent_level)
                result.append(tag)
                
                if not isClosing and not is_self_closing:
                    indent_level += 1
            else:
                result.append(tag)
            
            i = tagEnd + 1
        else:
            #Text content between tags  ("<p>Our Greenway</p> -> Our Greewany")
            textStart = i
            while i < len(htmlStr) and htmlStr[i] != "<":
                i += 1
            
            textContent = htmlStr[textStart:i].strip()
            if textContent:
                result.append(textContent)
    
    formatted = "".join(result)
    if formatted and not formatted.endswith("\n"):
        formatted += "\n"
    
    return formatted



def main():
    '''
    ---
    Main function for processing txt files.
    ---
    Usage: "python htmlClean.py input.txt output.txt"
        For some systems use "python3 htmlClean.py input.txt output.txt" if it doesn't work
    '''
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python htmlClean.py <input.txt> <output.txt>")
        print("Example: python htmlClean.py input.txt output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            html_content = f.read().strip()
        
        formatted_html = format_html_form(html_content)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(formatted_html)
        
        print(f"Successfully formatted HTML from '{input_file}' to '{output_file}'")
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()