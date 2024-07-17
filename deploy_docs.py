import os
import subprocess
import shutil

def generate_sphinx_docs():
    """Generate Sphinx documentation."""
    # Run sphinx-apidoc to generate .rst files
    subprocess.run(['sphinx-apidoc', '-o', 'docs/source/modules/', 'src/'], check=True)
    
    # Build HTML documentation
    subprocess.run(['make', '-C', 'docs', 'html'], check=True)

def generate_rust_docs():
    """Generate Rust documentation."""
    # Build Rust documentation
    subprocess.run(['cargo', 'doc', '--no-deps', '--document-private-items'], check=True)
    
    # Copy Rust docs to docs directory
    if os.path.exists('docs/rust'):
        shutil.rmtree('docs/rust')
    shutil.copytree('target/doc', 'docs/rust')

def prepare_gitbook():
    """Prepare Gitbook by copying Sphinx and Rust HTML output."""
    # Copy Sphinx HTML output to Gitbook source directory
    if os.path.exists('_book'):
        shutil.rmtree('_book')
    shutil.copytree('docs/build/html', '_book/sphinx')
    
    # Copy Rust HTML output to Gitbook source directory
    shutil.copytree('docs/rust', '_book/rust')

def build_gitbook():
    """Build Gitbook."""
    # Initialize Gitbook
    subprocess.run(['gitbook', 'install'], check=True)
    
    # Build Gitbook
    subprocess.run(['gitbook', 'build'], check=True)

def publish_gitbook():
    """Publish Gitbook to GitHub Pages."""
    # Publish Gitbook to GitHub Pages
    token = os.getenv('GITBOOK_TOKEN')
    if not token:
        raise EnvironmentError("GITBOOK_TOKEN environment variable not set")
    
    subprocess.run(['gitbook', 'publish', '.', '--token', token], check=True)

if __name__ == '__main__':
    generate_sphinx_docs()
    generate_rust_docs()
    prepare_gitbook()
    build_gitbook()
    publish_gitbook()
