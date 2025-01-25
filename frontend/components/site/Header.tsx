"use client"

import React from 'react'
import Link from 'next/link'

export const Header = () => {

    return (
        <header>
            <Link href="/">
                Home
            </Link>

            <style jsx>{`
        header {
          margin-bottom: 25px;
        }
        a {
          font-size: 14px;
          margin-right: 15px;
          text-decoration: none;
        }
        .is-active {
          text-decoration: underline;
        }
      `}</style>
        </header>
    )
}
