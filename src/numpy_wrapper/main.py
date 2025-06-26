"""A Dagger module for wrapping numpy functions."""

import dagger
from dagger import dag, function, object_type
import numpy as np


@object_type
class NumpyWrapper:
    @function
    def container_echo(self, string_arg: str) -> dagger.Container:
        """Returns a container that echoes whatever string argument is provided"""
        return dag.container().from_("alpine:latest").with_exec(["echo", string_arg])

    @function
    async def grep_dir(self, directory_arg: dagger.Directory, pattern: str) -> str:
        """Returns lines that match a pattern in the files of the provided Directory"""
        return await (
            dag.container()
            .from_("alpine:latest")
            .with_mounted_directory("/mnt", directory_arg)
            .with_workdir("/mnt")
            .with_exec(["grep", "-R", pattern, "."])
            .stdout()
        )

    @function
    def create_random_array(self, size: int = 5) -> str:
        """
        Creates a random square NumPy array of a given size and returns it as a string.
        """
        # Create a numpy array using the imported third-party library
        arr = np.random.rand(size, size)

        # Return the array as a string to make it JSON-serializable
        return np.array_str(arr)

    @function
    def matrix_multiply(self) -> str:
        """
        Creates and multiplies two 3x3 matrices and returns the result as a string.
        """
        matrix_a = np.arange(9).reshape(3, 3)
        matrix_b = np.arange(9).reshape(3, 3)
        result = np.matmul(matrix_a, matrix_b)
        return np.array_str(result)
