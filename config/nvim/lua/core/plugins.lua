-- plugins.lua
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({

    -- Treesitter
    { 'nvim-treesitter/nvim-treesitter', build = ":TSUpdate" },

    -- LSP
    { 'neovim/nvim-lspconfig' },
    { 'williamboman/mason.nvim' },

    -- Autocomplete
    { 'hrsh7th/nvim-cmp', lazy = false },
    { 'hrsh7th/cmp-nvim-lsp' },
    { 'hrsh7th/cmp-buffer' },
    { 'hrsh7th/cmp-path' },
    { 'hrsh7th/cmp-cmdline' },

    -- Telescope
    {
        'nvim-telescope/telescope.nvim', tag = '0.1.6',
        dependencies = { 'nvim-lua/plenary.nvim' }
    },

    -- Dashboard
    {
        'nvimdev/dashboard-nvim',
        event = 'VimEnter',
        dependencies = { 'nvim-tree/nvim-web-devicons' },
        config = function()
            require('dashboard').setup {}
        end
    },

    -- Visual
    { 'Eandrju/cellular-automaton.nvim' },
    { 'norcalli/nvim-colorizer.lua' },
    {
        'nvim-lualine/lualine.nvim',
        dependencies = { 'nvim-tree/nvim-web-devicons' }
    },

    -- Todo comments
    {
        "folke/todo-comments.nvim",
        dependencies = { "nvim-lua/plenary.nvim" },
        opts = {}
    },

    -- Themes
    { "ellisonleao/gruvbox.nvim", priority = 1000 , config = true },
    { "catppuccin/nvim", name = "catppuccin", priority = 1000 },

    -- Better Escape
   -- {
     --   "max397574/better-escape.nvim",
       -- config = function()
         --   require("better_escape").setup({
           --     mapping = {"jk"},
             --   timeout = vim.o.timeoutlen,
               -- clear_empty_lines = false,
             --   keys = "<Esc>",
          --  })
       -- end
   -- },

    -- Comments
    {
        'numToStr/Comment.nvim',
        lazy = false,
        opts = {}
    },

    -- Bufferline
    {'akinsho/bufferline.nvim', version = "*", dependencies = 'nvim-tree/nvim-web-devicons'},

    -- File explorer
    {
        "nvim-tree/nvim-tree.lua",
        version = "*",
        lazy = false,
        dependencies = { "nvim-tree/nvim-web-devicons" },
        config = function()
            require("nvim-tree").setup {}
        end,
    },

    -- Linting / ALE
    {
        'dense-analysis/ale',
        config = function()
            local g = vim.g
            g.ale_linters = {
                python = {'mypy'},
                lua = {'lua_language_server'}
            }
        end
    },

    -- Illuminate
    { 'RRethy/vim-illuminate' },

    -- LuaRocks
    {
        "vhyrro/luarocks.nvim",
        priority = 1001,
        opts = { rocks = { "magick" } }
    },

    -- Trouble
    {
        "folke/trouble.nvim",
        dependencies = { "nvim-tree/nvim-web-devicons" },
        opts = {}
    },

    -- Terminal
    {'akinsho/toggleterm.nvim', version = "*", config = true},

    -- Which-key
    {
        "folke/which-key.nvim",
        event = "VeryLazy",
        init = function()
            vim.o.timeout = true
            vim.o.timeoutlen = 300
        end,
        opts = {}
    },

    -- Mini plugins (text objects, movement, pairs)
    { 'echasnovski/mini.nvim', version = false },
    { 'echasnovski/mini.move', version = false },
    { 'echasnovski/mini.pairs', version = false },

})
