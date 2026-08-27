# Python Theatre Kontrol (PyTK)
**A Python framework for controlling theatre and live events equipment over a variety of protocols.**

## Features

- Provide a consistent interface for controlling show equipment across multiple protocols and manufacturers.
- Enable compatibility with a wide range of brands and equipment through modular device drivers.
- Standardise control operations across platforms — a Go command here should be a Go command there.
- Keep device-specific logic within drivers, allowing the core library to remain hardware agnostic.
- Make it easy to add support, standardise the library, make device support a driver, not the library itself.

I want to build a family of support leveraging drivers to control a huge range of equipment, I want it to be quick and easy to build drivers to add support for hardware that fits into a supported category.

### A quick note on vocabulary
This library, at least the lighting framework, uses ETC Eos vocabulary under the hood, that's because that's what I programme on most, so like a first language, my brain thinks in eos syntax primarily. Hopefully that isn't too confusing, and I hope to find better descriptors where required in the future.


## Roadmap
Please refer to markdown file [ROADMAP.md](docs/ROADMAP.md) for the project roadmap and future plans.

## Scope of support
My goal is to
1) Support as much as possible, from projectors to consoles, to from sound to AV, with standardised support everywhere.
2) Make it easy to add support, leveraging python Protocols to build device drivers
3) Make it simple to migrate from one platform to another, a projector swap shouldn't necessitate rewriting half your software, all it should need is the change of a variable to load a different driver (Assuming that both pieces of hardware have the same capabilities)

In an ideal world, it shouldn't matter if you are using OSC, TCP, Serial, or a carrier pigeon, the command should be the same from a user perspective. 

## Feature requests
If you have any feature requests or suggestions, please feel free to open an issue on our GitHub repository. I will be prioritising features based on my requirements and user feedback, so your input is highly valuable.

## Contributing
Contributions to PyTK are welcome! If you would like to contribute, please follow these steps:
1. Fork the repository and create a new branch for your feature or bug fix.
2. Make your changes and ensure that they are well-documented and tested.
3. Submit a pull request with a clear description of your changes and the problem they solve.
4. I will review your pull request and provide feedback or merge it if it meets the project's standards.

## License
PyTK is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## AI Assistance Policy
While I have and do continue to use AI tools to assist with the development of Python Theatre Kontrol, this project is by no means an AI-generated or vibe coded project. I am the sole maintainer and primary developer, and I take maintainability and support of my projects very seriously. I personally use AI tools to assist with problem solving, and creating of simple code snippets, especially for things that I'm not particularly familiar with, things like regex. However AI tools have not been used to generate large portions of this codebase. And I personally review or perfect nearly every line of code that I publish. I don't belive AI generated code to be a perfect solution, especially in the scope of maintainability, reliability and security. Should you choose to contribute to this project, I would kindly ask that you follow a similar approach to the use of AI tools as I myself do, that it is a tool and not a crutch.

## Contact
If you have any questions, suggestions, or just want to chat about the project, feel free to reach out to me via the means of a GitHub Issue.
