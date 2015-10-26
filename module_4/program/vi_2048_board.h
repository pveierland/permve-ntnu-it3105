#ifndef VI_2048_BOARD_H
#define VI_2048_BOARD_H

#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <limits>
#include <ostream>
#include <vector>

namespace vi
{
    enum class action : unsigned
    {
        up    = 0,
        down  = 1,
        left  = 2,
        right = 3
    };

    struct board
    {
        using row       = std::uint16_t;
        using state     = std::uint64_t;
        using heuristic = float;
        using score     = float;

        static constexpr unsigned lut_size = std::numeric_limits<row>::max() + 1;

        struct move_luts
        {
            std::vector<state> up, down;
            std::vector<row>   left, right;
        };

        static std::vector<heuristic> build_heuristic_lut();
        static move_luts              build_move_lut();
        static std::vector<score>     build_score_lut();
        static row                    reverse_row(row);
        static state                  transpose_board(state);
        static state                  unpack_column(row);

        board(const state board_state = 0)
            : board_state(board_state) { }
        board(const board&) = default;

        board     move(action) const;
        board     spawn(unsigned row, unsigned column, unsigned value) const;
        heuristic get_heuristic() const;
        score     get_score() const;
        unsigned  get_available_count() const;
        unsigned  get_highest_raw_value() const;
        unsigned  get_highest_value() const;
        unsigned  get_raw_value(unsigned row, unsigned column) const;
        unsigned  get_value(unsigned row, unsigned column) const;
        void      set_raw_value(unsigned row, unsigned column, unsigned raw_value);
        void      set_value(unsigned row, unsigned column, unsigned value);

        static std::vector<heuristic> heuristic_lut;
        static std::vector<score>     score_lut;
        static move_luts              move_lut;

        state board_state;
    };

    std::ostream& operator<<(std::ostream&, const board&);

    inline
    bool
    operator==(const board& a, const board& b)
    {
        return a.board_state == b.board_state;
    }

    inline
    bool
    operator!=(const board& a, const board& b)
    {
        return a.board_state != b.board_state;
    }

    inline
    board::row
    board::reverse_row(const board::row row)
    {
        return ((row & 0xF000U) >> 12) | ((row & 0x0F00U) >> 4) |
               ((row & 0x000FU) << 12) | ((row & 0x00F0U) << 4);
    }

    inline
    board::state
    board::transpose_board(const board::state board_state)
    {
        const auto a1 = board_state & 0xF0F00F0FF0F00F0FULL;
        const auto a2 = board_state & 0x0000F0F00000F0F0ULL;
        const auto a3 = board_state & 0x0F0F00000F0F0000ULL;
        const auto a  = a1 | (a2 << 12) | (a3 >> 12);
        const auto b1 = a & 0xFF00FF0000FF00FFULL;
        const auto b2 = a & 0x00FF00FF00000000ULL;
        const auto b3 = a & 0x00000000FF00FF00ULL;
        return b1 | (b2 >> 24) | (b3 << 24);
    }

    inline
    board::state
    board::unpack_column(const board::row row)
    {
        return 0x000F000F000F000FULL &
            ((static_cast<board::state>(row) <<  0) |
             (static_cast<board::state>(row) << 12) |
             (static_cast<board::state>(row) << 24) |
             (static_cast<board::state>(row) << 36));
    }

    // From https://github.com/nneonneo/2048-ai/blob/master/2048.cpp
    inline
    unsigned
    board::get_available_count() const
    {
        auto x = board_state;
        x |= (x >> 2) & 0x3333333333333333ULL;
        x |= (x >> 1);
        x = ~x & 0x1111111111111111ULL;
        // At this point each nibble is:
        //  0 if the original nibble was non-zero
        //  1 if the original nibble was zero
        // Next sum them all
        x += x >> 32;
        x += x >> 16;
        x += x >>  8;
        x += x >>  4; // this can overflow to the next nibble if there were 16 empty positions
        return static_cast<unsigned>(x & 0xF);
    }

    inline
    board::heuristic
    board::get_heuristic() const
    {
        const auto transposed_state = transpose_board(board_state);

        return (heuristic_lut[(board_state      >>  0) & 0xFFFFU] +
                heuristic_lut[(board_state      >> 16) & 0xFFFFU] +
                heuristic_lut[(board_state      >> 32) & 0xFFFFU] +
                heuristic_lut[(board_state      >> 48) & 0xFFFFU] +
                heuristic_lut[(transposed_state >>  0) & 0xFFFFU] +
                heuristic_lut[(transposed_state >> 16) & 0xFFFFU] +
                heuristic_lut[(transposed_state >> 32) & 0xFFFFU] +
                heuristic_lut[(transposed_state >> 48) & 0xFFFFU]);
    }

    inline
    unsigned
    board::get_highest_raw_value() const
    {
        unsigned highest_raw = 0;
        state tmp = board_state;

        for (unsigned i = 0; i != 16; ++i)
        {
            const auto raw_value = tmp & 0xFU;
            if (raw_value > highest_raw)
            {
                highest_raw = raw_value;
            }
            tmp >>= 4;
        }

        return highest_raw;
    }

    inline
    unsigned
    board::get_highest_value() const
    {
        const auto raw = get_highest_raw_value();
        return raw ? 1 << raw : 0;
    }
    
    inline
    unsigned
    board::get_raw_value(const unsigned row, const unsigned column) const
    {
        const auto offset = 16U * row + 4U * column;
        return (board_state >> offset) & 0xFU;
    }

    inline
    board::score
    board::get_score() const
    {
        return score_lut[(board_state >>  0) & 0xFFFFU] +
               score_lut[(board_state >> 16) & 0xFFFFU] +
               score_lut[(board_state >> 32) & 0xFFFFU] +
               score_lut[(board_state >> 48) & 0xFFFFU];
    }
    
    inline
    unsigned
    board::get_value(const unsigned row, const unsigned column) const
    {
        const auto raw = get_raw_value(row, column);
        return raw ? 1 << raw : 0;
    }

    inline
    board
    board::move(const vi::action action) const
    {
        switch (action)
        {
            case vi::action::up:
            {
                const auto transposed_state = transpose_board(board_state);
                return board{board_state ^
                    (move_lut.up[(transposed_state >>  0) & 0xFFFFU] <<  0) ^
                    (move_lut.up[(transposed_state >> 16) & 0xFFFFU] <<  4) ^
                    (move_lut.up[(transposed_state >> 32) & 0xFFFFU] <<  8) ^
                    (move_lut.up[(transposed_state >> 48) & 0xFFFFU] << 12)};
            }
            case vi::action::down:
            {
                const auto transposed_state = transpose_board(board_state);
                return board{board_state ^
                    (move_lut.down[(transposed_state >>  0) & 0xFFFFU] <<  0) ^
                    (move_lut.down[(transposed_state >> 16) & 0xFFFFU] <<  4) ^
                    (move_lut.down[(transposed_state >> 32) & 0xFFFFU] <<  8) ^
                    (move_lut.down[(transposed_state >> 48) & 0xFFFFU] << 12)};
            }
            case vi::action::left:
            {
                return board{board_state ^
                    (static_cast<board::state>(move_lut.left[(board_state >>  0) & 0xFFFFU]) <<  0) ^
                    (static_cast<board::state>(move_lut.left[(board_state >> 16) & 0xFFFFU]) << 16) ^
                    (static_cast<board::state>(move_lut.left[(board_state >> 32) & 0xFFFFU]) << 32) ^
                    (static_cast<board::state>(move_lut.left[(board_state >> 48) & 0xFFFFU]) << 48)};
            }
            case vi::action::right:
            {
                return board{board_state ^
                    (static_cast<board::state>(move_lut.right[(board_state >>  0) & 0xFFFFU]) <<  0) ^
                    (static_cast<board::state>(move_lut.right[(board_state >> 16) & 0xFFFFU]) << 16) ^
                    (static_cast<board::state>(move_lut.right[(board_state >> 32) & 0xFFFFU]) << 32) ^
                    (static_cast<board::state>(move_lut.right[(board_state >> 48) & 0xFFFFU]) << 48)};
            }
            default:
            {
                assert(0);
            }
        }
    }

    inline
    void
    board::set_raw_value(const unsigned row, const unsigned column, const unsigned raw_value)
    {
        const auto offset = 16U * row + 4U * column;
        board_state = (board_state & ~(0x15U << offset)) | (raw_value << offset);
    }

    inline
    void
    board::set_value(const unsigned row, const unsigned column, const unsigned value)
    {
        const auto raw_value = value ? static_cast<unsigned>(std::log2(value)) : 0;
        set_raw_value(row, column, raw_value);
    }

    inline
    board
    board::spawn(const unsigned row, const unsigned column, const unsigned value) const
    {
        auto new_board = board{*this};
        new_board.set_value(row, column, value);
        return new_board;
    }
}

namespace std
{
    template <>
    struct hash<::vi::board>
    {
        using argument_type = ::vi::board;
        using result_type   = std::size_t;

        inline
        result_type
        operator()(const argument_type& board) const
        {
            return board.board_state;
        }
    };
}

#endif // VI_2048_BOARD_H

