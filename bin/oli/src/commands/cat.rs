// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

use anyhow::Result;
use futures::io;

use crate::config::Config;
use crate::make_tokio_runtime;
use crate::params::config::ConfigParams;

#[derive(Debug, clap::Parser)]
#[command(
    name = "cat",
    about = "Display object content",
    disable_version_flag = true
)]
pub struct CatCmd {
    #[command(flatten)]
    pub config_params: ConfigParams,
    /// In the form of `<profile>:/<path>`.
    #[arg()]
    pub target: String,
}

impl CatCmd {
    pub fn run(self) -> Result<()> {
        make_tokio_runtime(1).block_on(self.do_run())
    }

    async fn do_run(self) -> Result<()> {
        let cfg = Config::load(&self.config_params.config)?;

        let (op, path) = cfg.parse_location(&self.target)?;

        let reader = op.reader(&path).await?;
        let meta = op.stat(&path).await?;
        let mut buf_reader = reader
            .into_futures_async_read(0..meta.content_length())
            .await?;
        let mut stdout = io::AllowStdIo::new(std::io::stdout());
        io::copy_buf(&mut buf_reader, &mut stdout).await?;
        Ok(())
    }
}
