"""Regenera los bindings Python de gRPC a partir de product.proto."""

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROTO_DIR = PROJECT_ROOT / "services" / "products" / "grpc" / "proto"
GENERATED_DIR = PROJECT_ROOT / "services" / "products" / "grpc" / "generated"
PROTO_FILE = PROTO_DIR / "product.proto"


def main() -> None:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            sys.executable,
            "-m",
            "grpc_tools.protoc",
            f"-I{PROTO_DIR}",
            f"--python_out={GENERATED_DIR}",
            f"--grpc_python_out={GENERATED_DIR}",
            str(PROTO_FILE),
        ],
        check=True,
        cwd=PROJECT_ROOT,
    )

    grpc_file = GENERATED_DIR / "product_pb2_grpc.py"
    content = grpc_file.read_text(encoding="utf-8")
    content = content.replace(
        "import product_pb2 as product__pb2",
        "from services.products.grpc.generated import product_pb2 as product__pb2",
    )
    grpc_file.write_text(content, encoding="utf-8")

    print("Bindings gRPC regenerados correctamente.")


if __name__ == "__main__":
    main()
