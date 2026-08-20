from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProcessResult:
    """
    Representa el resultado de la ejecución de un proceso del sistema.

    Attributes:
        success:
            Indica si el proceso terminó correctamente.

        output:
            Salida estándar generada por el proceso.

        error:
            Mensaje de error producido durante la ejecución.
    """

    success: bool = False
    output: list[str] = field(default_factory=list)
    error: str | None = None