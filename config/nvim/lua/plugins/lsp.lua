local capabilities = require("cmp_nvim_lsp").default_capabilities()

-- Python
vim.lsp.config.pyright = {
    capabilities = capabilities,
    settings = {
        pyright = { disableOrganizeImports = true },
        python = { analysis = { ignore = { "*" } } },
    },
}
vim.lsp.enable('pyright')

-- TypeScript
vim.lsp.config.ts_ls = {
    capabilities = capabilities,
}
vim.lsp.enable('ts_ls')

-- Rust
vim.lsp.config.rust_analyzer = {
    capabilities = capabilities,
    settings = { ["rust-analyzer"] = {} },
}
vim.lsp.enable('rust_analyzer')

-- Ruff
vim.lsp.config.ruff = {
    capabilities = capabilities,
    init_options = {
        settings = {
            args = {
                "--select=E,F,UP,N,I,ASYNC,S,PTH",
                "--line-length=79",
                "--respect-gitignore",
                "--target-version=py311"
            },
        },
    },
}
vim.lsp.enable('ruff')
